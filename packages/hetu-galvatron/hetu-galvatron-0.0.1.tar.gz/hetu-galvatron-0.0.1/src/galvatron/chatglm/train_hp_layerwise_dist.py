import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from .dataloader import DataLoaderForChatGLM
from transformers import AutoModel, AutoConfig
from tqdm import tqdm
import numpy as np
import random
import time
import sys
from .hybrid_parallel_model_dist import get_hybrid_parallel_configs, construct_hybrid_parallel_model, overwrite_megatron_args
from ..utils import print_peak_memory, save_profiled_memory
from megatron.initialize import initialize_megatron
from megatron import get_args
from torch.utils.data.distributed import DistributedSampler
from typing import Tuple, List

torch.backends.cudnn.allow_tf32 = True
torch.backends.cuda.matmul.allow_tf32 = True

def set_seed():
    seed = 123
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

def loss_func(labels, outputs):
    loss_fct = nn.CrossEntropyLoss()
    lm_logits = outputs[0]
    labels = labels[0]

    loss = None
    lm_logits = lm_logits.to(torch.float32)

    # Shift so that tokens < n predict n
    shift_logits = lm_logits[..., :-1, :].contiguous()
    shift_labels = labels[..., 1:].contiguous()
    # Flatten the tokens
    loss_fct = nn.CrossEntropyLoss(ignore_index=-100)
    loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

    # lm_logits = lm_logits.to(hidden_states.dtype)
    # loss = loss.to(hidden_states.dtype)
    
    return loss

def forward_step_func(inputs, model):
    if isinstance(inputs, (Tuple, List)):
        outputs = model(*inputs)
    else:
        outputs = model(inputs)
    return outputs, loss_func

def train(args):
    local_rank = args.local_rank
    rank = torch.distributed.get_rank()
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    world_size = torch.distributed.get_world_size()

    hybrid_parallel_configs = get_hybrid_parallel_configs(args)

    config = AutoConfig.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    overwrite_config = {'hidden_size': args.hidden_size,
                        'inner_hidden_size': args.hidden_size*4,
                        'max_sequence_length': args.seq_length,
                        'num_attention_heads': args.num_attention_heads,
                        'num_layers': args.num_hidden_layers,
                        'vocab_size': args.vocab_size}
    
    for key, val in overwrite_config.items():
        setattr(config, key, val)
    
    overwrite_config = {'use_flash_attn': args.use_flash_attn}
    
    for key, val in overwrite_config.items():
        setattr(config, key, val)
    # if local_rank == 0:
    #     print("Model Config:")
    #     print(config)
    overwrite_megatron_args(config, args)

    if local_rank == 0:
        print("Creating Dataloader...")
    dataset = DataLoaderForChatGLM(args, config)
    data_num_replicas = world_size // hybrid_parallel_configs['pp_deg']
    train_batch_size_input = args.global_train_batch_size // data_num_replicas
    trainloader = DataLoader(dataset=dataset,
                            batch_size=train_batch_size_input,
                            sampler=DistributedSampler(dataset,shuffle=True,num_replicas=data_num_replicas,rank=rank%data_num_replicas))

    if local_rank == 0:
        print("Creating Model...")
    
    chatglm_model = AutoModel.from_config(config, trust_remote_code=True)
    # if local_rank == 0:
    #     print(chatglm_model)
    model = construct_hybrid_parallel_model(model=chatglm_model,
                                            model_config=config,
                                            training_args=args,
                                            hybrid_parallel_configs=hybrid_parallel_configs)
    optimizer = Adam(model.parameters(), lr=args.lr, weight_decay=args.adam_weight_decay)

    # profile_rank = 0 # profile first stage memory
    profile_ranks = [0,world_size-1]
    if args.profile and rank in profile_ranks:
        print_peak_memory("After creating model", local_rank, args.profile_type)

    start_iter, end_iter = 7, 12
     # profile first stage memory
    # profile_rank = 7 # profile last stage memory
    mem_dict = {}
    total_iter = 0
    if local_rank == 0:
        print("Start training...")
    for ep in range(args.epochs):
        if not args.check_loss and not args.profile:
            trainloader = tqdm(trainloader)
        for iter, batch in enumerate(trainloader):
            start_time = time.time()
            if args.profile:
                if iter == start_iter:
                    total_start_time = start_time
                elif iter == end_iter:
                    total_end_time = start_time
                    avg_time = (total_end_time-total_start_time)/(end_iter-start_iter)
                    print("Average iteration time is: %.4f s"%avg_time)
                    return

            input_ids, labels = [tensor.to(device) for tensor in batch]
            batch = [[input_ids], [labels]]

            if args.profile and rank in profile_ranks and iter <= 5:
                torch.cuda.reset_peak_memory_stats(local_rank)
                max_mem, cur_mem = print_peak_memory("\nBefore Forward", local_rank, args.profile_type)
                if iter <= 4:
                    mem_dict['iter_%d_before_forward'%iter] = cur_mem

            if args.pipeline_type == "gpipe":
                loss = model.gpipe_forward(forward_step_func, batch)

                if args.profile and rank in profile_ranks and iter <= 5:
                    max_mem, cur_mem = print_peak_memory("After Forward", local_rank, args.profile_type)
                    if iter <= 4:
                        mem_dict['iter_%d_after_forward'%iter] = cur_mem

                model.gpipe_backward()
            elif args.pipeline_type == "pipedream_flush":
                loss = model.pipedream_flush_forward_backward(forward_step_func, batch)
            else:
                raise NotImplementedError

            if args.profile and rank in profile_ranks and iter <= 5:
                max_mem, cur_mem = print_peak_memory("After Backward", local_rank, args.profile_type)
                if iter <= 4:
                    mem_dict['iter_%d_after_backward'%iter] = cur_mem
                    mem_dict['iter_%d_after_backward_max'%iter] = max_mem

            optimizer.step()

            if args.profile and rank in profile_ranks and iter <= 5:
                max_mem, cur_mem = print_peak_memory("After optimizer_step", local_rank, args.profile_type)

            optimizer.zero_grad()

            end_time = time.time()
            total_iter = total_iter + 1
            if args.check_loss or args.profile:
                if len(loss):
                    loss = np.mean([l.item() for l in loss])
                    print('[Epoch %d] (Iteration %d): Loss = %.3f'% (ep,iter,loss.item()))

            if args.profile and iter == 5:
                if rank in profile_ranks:
                    mem_dict['model_states'] = mem_dict['iter_4_after_backward']
                    if args.pipeline_type == "gpipe":
                        mem_dict['model_states_and_activation'] = mem_dict['iter_4_after_forward']
                        mem_dict['activation'] = mem_dict['iter_4_after_forward'] - mem_dict['iter_4_before_forward']
                    mem_dict['model_states_and_peak_activation'] = mem_dict['iter_4_after_backward_max']
                    mem_dict['peak_activation'] = mem_dict['iter_4_after_backward_max'] - mem_dict['iter_4_after_backward']
                    time.sleep(0.2*rank)
                    print('[Profiled memory for rank %d]:'%rank)
                    for key, val in mem_dict.items():
                        print("\t%s: %.2f MB"%(key, val))
                    if args.save_profiled_memory:
                        precision = args.mixed_precision + '_'
                        memory_config_path = './configs/memory_profiling_%dgpus_dist_%shidden%d_head%d_seqlen%d.json'%(world_size, precision, args.hidden_size, args.num_attention_heads, args.seq_length)
                        save_profiled_memory(memory_config_path, args.pp_deg, args.global_tp_deg, world_size, args.num_hidden_layers, \
                                            args.global_train_batch_size, rank, mem_dict['model_states'], mem_dict['activation'], mem_dict['peak_activation'], args.global_checkpoint)


def add_arguments(parser):
    group = parser.add_argument_group(title='our arguments')

    group.add_argument(
        "--local-rank", type=int, default=-1, help="Local rank.",
    )
    group.add_argument(
        "--global_train_batch_size", type=int, default=32, help="Global training batch size"
    )
    group.add_argument(
        "--hidden_size", type=int, default=1280, help="Hidden size of transformer model",
    )
    group.add_argument(
        "--num_hidden_layers", type=int, default=12, help="Number of layers"
    )
    group.add_argument(
        "-a",
        "--num_attention_heads",
        type=int,
        default=32,
        help="Number of attention heads",
    )
    group.add_argument(
        "-s", "--seq_length", type=int, default=128, help="Maximum sequence len"
    )
    group.add_argument(
        "--vocab_size", type=int, default=51865, help="Total number of vocab"
    )
    group.add_argument(
        "--dropout_prob", type=float, default=0.1, help="Dropout rate."
    )
    group.add_argument("-e", "--epochs", type=int,
                        default=10, help="Number of epochs")
    group.add_argument(
        "--adam_weight_decay", type=float, default=0.01, help="Weight_decay of adam"
    )

    group.add_argument(
        "--check_loss", type=int, default=0, help="Whether to check model correctness."
    )
    group.add_argument(
        "--profile", type=int, default=0, help="Whether to profile model GPU memory."
    )
    group.add_argument(
        "--save_profiled_memory", type=int, default=0, help="Whether to save profiled memory."
    )
    group.add_argument(
        "--profile_type", type=str, default='allocated', help="Profile allocated memory or reserved memory.",
        choices = ['allocated', 'reserved'],
    )
    parser.add_argument(
        "--load_params", type=int, default=0, help="Whether to load saved init params."
    )
    parser.add_argument(
        "--pp_deg", type=int, default=2, help="Pipeline parallel degree.", choices=[1,2,4,8,16,32,64],
    )
    parser.add_argument(
        "--global_tp_deg", type=int, default=-1, help="Global tensor parallel degree.", choices=[-1,1,2,4,8,16,32],
    )
    parser.add_argument(
        "--chunks", type=int, default=-1, help="Pipeline chunk num.",
    )
    parser.add_argument(
        "--global_tp_consec", type=int, default=-1, help="Global tensor parallel group consecutive flag."
    )
    parser.add_argument(
        "--fsdp", type=int, default=0, help="Apply FSDP", choices=[0, 1],
    )
    parser.add_argument(
        "--apply_strategy", type=int, default=0, help="Apply searched strategy.", choices=[0, 1],
    )
    parser.add_argument(
        "--galvatron_config_path", type=str, default=None, help="Galvatron strategy config path. If not None, galvatron will run according to json config file.",
    )
    parser.add_argument(
        "--global_checkpoint", type=int, default=0, help="Global checkpoint flag."
    )
    parser.add_argument(
        "--mixed_precision", type=str, default='bf16', help="Mixed precision option.", choices=['fp32', 'fp16', 'bf16'],
    )
    parser.add_argument(
        "--pipeline_type", type=str, default="gpipe", help="Galvatron pipeline type", choices=["gpipe","pipedream_flush"],
    )
    parser.add_argument(
        "--default_dp_type", type=str, default="zero2", help="Default data parallel type", choices=["ddp","zero2"],
    )
    return parser

if __name__ == '__main__':
    initialize_megatron(extra_args_provider=add_arguments)
    args = get_args()
    set_seed()
    train(args)

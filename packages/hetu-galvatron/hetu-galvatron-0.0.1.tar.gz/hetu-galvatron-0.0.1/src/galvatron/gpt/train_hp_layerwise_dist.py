import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from .dataloader import DataLoaderForGPT
import argparse
from tqdm import tqdm
import numpy as np
import random
import h5py
import time
import os
import sys
from ..utils import print_peak_memory
from megatron.initialize import initialize_megatron
from megatron import get_args
from torch.utils.data.distributed import DistributedSampler
from typing import Tuple, List
from .hybrid_parallel_model_dist import get_hybrid_parallel_configs, construct_hybrid_parallel_model, overwrite_megatron_args
from ..utils import save_profiled_memory, print_param_num
from flash_attn.models.gpt import GPTLMHeadModel
from .gpt_config_utils import gpt_config, overwrite_configs_and_args

torch.backends.cudnn.allow_tf32 = True
torch.backends.cuda.matmul.allow_tf32 = True

def set_seed():
    seed = 123
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

def loss_func(labels, outputs):
    return outputs[0]

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
    
    config = gpt_config(args)
    overwrite_configs_and_args(config, args)
    overwrite_megatron_args(config, args)

    hybrid_parallel_configs = get_hybrid_parallel_configs(args)

    if local_rank == 0:
        print("Creating Dataloader...")
    dataset = DataLoaderForGPT(args)
    data_num_replicas = world_size // hybrid_parallel_configs['pp_deg']
    train_batch_size_input = args.global_train_batch_size // data_num_replicas
    trainloader = DataLoader(dataset=dataset,
                            batch_size=train_batch_size_input,
                            sampler=DistributedSampler(dataset,shuffle=True,num_replicas=data_num_replicas,rank=rank%data_num_replicas))

    if local_rank == 0:
        print("Creating Model...")

    gpt_model = GPTLMHeadModel(config, device='meta' if args.initialize_on_meta else 'cpu')
    model = construct_hybrid_parallel_model(model=gpt_model, 
                                            model_config=config, 
                                            training_args=args, 
                                            hybrid_parallel_configs=hybrid_parallel_configs)
    optimizer = Adam(model.parameters(), lr=args.lr, weight_decay=args.adam_weight_decay)
    
    if rank == 0:
        print(config)
        print_param_num(model)

    # profile_rank = 0 # profile first stage memory
    profile_ranks = [0,world_size-1]
    if args.profile and rank in profile_ranks:
        print_peak_memory("After creating model", local_rank, args.profile_type)

    start_iter, end_iter = 7, 13
     # profile first stage memory
    # profile_rank = 7 # profile last stage memory
    mem_dict = {}
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
            input_ids = batch.to(device)
            batch = [[input_ids], [input_ids]]

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
                # return

def add_arguments(parser):
    group = parser.add_argument_group(title='our arguments')

    group.add_argument(
        "--local-rank", type=int, default=-1, help="Local rank.",
    )
    parser.add_argument(
        "--model_size", type=str, default='gpt-1.5b', help="Model size.", choices=['gpt-1.5b', 'gpt-2.7b', 'gpt-6.7b']
    )
    parser.add_argument(
        "--overwrite_config", type=int, default=0, help="Whether to overwrite model config"
    )
    group.add_argument(
        "--initialize_on_meta", type=int, default=1, help="Whether to initialize parameters on meta device.", choices=[0, 1]
    )
    group.add_argument(
        "--global_train_batch_size", type=int, default=32, help="Global training batch size"
    )
    group.add_argument(
        "--hidden_size", type=int, default=768, help="Hidden size of transformer model",
    )
    group.add_argument(
        "--num_hidden_layers", type=int, default=12, help="Number of layers"
    )
    group.add_argument(
        "-a",
        "--num_attention_heads",
        type=int,
        default=12,
        help="Number of attention heads",
    )
    group.add_argument(
        "-s", "--seq_length", type=int, default=128, help="Maximum sequence len"
    )
    group.add_argument(
        "--vocab_size", type=int, default=30522, help="Total number of vocab"
    )
    group.add_argument(
        "--dropout_prob", type=float, default=0.1, help="Dropout rate."
    )
    group.add_argument("--max_predictions_per_seq", type=int, default=20)
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
        "--default_dp_type", type=str, default="zero2", help="Default data parallel type", choices=["ddp","zero2","zero3"],
    )
    return parser

if __name__ == '__main__':
    initialize_megatron(extra_args_provider=add_arguments)
    args = get_args()
    set_seed()
    train(args)

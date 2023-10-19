import torch
from torch import nn
from torch.utils.data import DataLoader
from .dataloader import DataLoaderForChatGLM
from transformers import AutoModel, AutoConfig
import numpy as np
import random
import os
import sys
from ..utils import read_json_config, write_json_config
from megatron.initialize import initialize_megatron
from megatron import get_args
from .hybrid_parallel_model_dist import overwrite_megatron_args
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.api import ShardingStrategy, MixedPrecision, BackwardPrefetch

torch.backends.cudnn.allow_tf32 = True
torch.backends.cuda.matmul.allow_tf32 = True

def set_seed():
    seed = 123
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

def model_forward(model, input_ids, labels):
    lm_logits = model(input_ids).logits
    loss_fct = nn.CrossEntropyLoss()

    loss = None
    lm_logits = lm_logits.to(torch.float32)

    # Shift so that tokens < n predict n
    shift_logits = lm_logits[..., :-1, :].contiguous()
    shift_labels = labels[..., 1:].contiguous()
    # Flatten the tokens
    loss_fct = nn.CrossEntropyLoss(ignore_index=-100)
    loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

    return loss

def construct_fsdp_model(model, device):
    # rriginal model has all torch.half params_dtype except layernorms
    glm_model = model.transformer
    glm_model.final_layernorm = nn.LayerNorm(glm_model.hidden_size, eps=glm_model.layernorm_epsilon, dtype=torch.half)
    for block in glm_model.layers:
        block.input_layernorm = nn.LayerNorm(glm_model.hidden_size, eps=glm_model.layernorm_epsilon, dtype=torch.half)
        block.post_attention_layernorm = nn.LayerNorm(glm_model.hidden_size, eps=glm_model.layernorm_epsilon, dtype=torch.half)

    mixed_precision = {'fp32': torch.float, 'fp16': torch.float16, 'bf16': torch.bfloat16}[args.mixed_precision]
    mixed_precision_policy = MixedPrecision(
        param_dtype=mixed_precision, # Param precision
        reduce_dtype=mixed_precision, # Gradient communication precision
        buffer_dtype=mixed_precision, # Buffer precision
        cast_forward_inputs=True,
        cast_root_forward_inputs=True
    )
    fsdp_args = dict(sharding_strategy = ShardingStrategy.NO_SHARD, 
                    mixed_precision=mixed_precision_policy, 
                    backward_prefetch=None,
                    auto_wrap_policy=None)

    model = model.to(device)
    model = FSDP(model, **fsdp_args)
    return model

def run_forward(args):
    local_rank = args.local_rank
    cuda_condition = torch.cuda.is_available()
    device = torch.device("cuda:%d"%args.gpu_id if cuda_condition else "cpu")
    rank = args.gpu_id

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
    
    overwrite_megatron_args(config, args)

    print("Creating Dataloader...")
    dataset = DataLoaderForChatGLM(args, config)
    trainloader = DataLoader(dataset=dataset,
                            batch_size=args.train_batch_size,
                            shuffle=False)

    print("Creating Model...")
    
    chatglm_model = AutoModel.from_config(config, trust_remote_code=True)
    model = construct_fsdp_model(chatglm_model, device)
    
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start_iter, end_iter = 10, 20
    
    print("Profiling...")
    time_list = []
    for ep in range(args.epochs):
        for iter, batch in enumerate(trainloader):
            if iter == end_iter:
                avg_time = sum(time_list) / len(time_list) / args.train_batch_size
                print("Average forward computation time of %d ChatGLM layers (hidden_size=%d) is: %.4f ms / bsz"%(args.num_hidden_layers, args.hidden_size, avg_time))
                return avg_time
            input_ids, labels = [tensor.to(device) for tensor in batch]
            torch.cuda.synchronize()
            start.record()
            model_forward(model, input_ids, labels)
            end.record()
            torch.cuda.synchronize()
            iter_time = start.elapsed_time(end)
            if iter >= start_iter:
                time_list.append(iter_time)


def profile(args):
    args.num_hidden_layers = 8
    time_8_layers = run_forward(args)
    args.num_hidden_layers = 4
    time_4_layers = run_forward(args)
    time_per_layer = (time_8_layers-time_4_layers)/4

    fwd_config_path = './configs/forward_profiling_config.json'
    config = read_json_config(fwd_config_path) if os.path.exists(fwd_config_path) else dict()
    mp = '_'+args.mixed_precision
    key = 'fwd_time%s_hidden_%d'%(mp, args.hidden_size)
    config[key] = time_per_layer
    print('********************')
    print("Average forward computation time of ChatGLM layer (hidden_size=%d) is: %.4f ms / layer / bsz"%(args.hidden_size, time_per_layer))
    write_json_config(config, fwd_config_path)
    print('Already written forward profiling config into env config file %s!\n'%(fwd_config_path))


def add_arguments(parser):
    group = parser.add_argument_group(title='our arguments')

    group.add_argument(
        '--gpu_id', type=int, default=0, help='Id of GPU to run.'
    )
    group.add_argument(
        "--train_batch_size", type=int, default=32, help="Global training batch size"
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
        default=20,
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
    parser.add_argument(
        "--mixed_precision", type=str, default='bf16', help="Mixed precision option.", choices=['fp32', 'fp16', 'bf16'],
    )
    return parser

if __name__ == '__main__':
    initialize_megatron(extra_args_provider=add_arguments)
    args = get_args()
    set_seed()
    profile(args)

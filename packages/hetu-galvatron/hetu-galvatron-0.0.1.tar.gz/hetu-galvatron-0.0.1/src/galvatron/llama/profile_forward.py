import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from .dataloader import DataLoaderForLlama
import argparse
from tqdm import tqdm
import numpy as np
import random
import h5py
import time
import os
import sys
from ..utils import print_peak_memory
from transformers.models.gpt2.configuration_gpt2 import GPT2Config
from flash_attn.models.gpt import GPTLMHeadModel
from ..utils import print_peak_memory
from ..utils import read_json_config, write_json_config
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.api import ShardingStrategy, MixedPrecision, BackwardPrefetch
from .llama_config_utils import llama_config_to_gpt2_config, config_from_checkpoint, overwrite_configs_and_args


def set_seed():
    seed = 123
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

def model_forward(model, input_ids):
    lm_logits = model(input_ids=input_ids).logits
    shift_logits = lm_logits[..., :-1, :].contiguous()
    shift_labels = input_ids[..., 1:].contiguous()
    from flash_attn.losses.cross_entropy import CrossEntropyLoss
    loss_fn = CrossEntropyLoss()
    loss = loss_fn(shift_logits.view(-1, model.config.vocab_size), shift_labels.view(-1).long())
    return loss

def construct_fsdp_model(model, device):
    mixed_precision = {'fp32': torch.float, 'fp16': torch.float16, 'bf16': torch.bfloat16}[args.mixed_precision]
    mixed_precision_policy = MixedPrecision(
        param_dtype=mixed_precision, # Param precision
        reduce_dtype=mixed_precision, # Gradient communication precision
        buffer_dtype=mixed_precision, # Buffer precision
        cast_forward_inputs=True,
        cast_root_forward_inputs=True
    )
    backward_prefetch=None
    fsdp_args = dict(sharding_strategy = ShardingStrategy.NO_SHARD, 
                    mixed_precision=mixed_precision_policy, 
                    backward_prefetch=None,
                    auto_wrap_policy=None)

    model = model.to(device)
    model = FSDP(model, **fsdp_args)
    return model

def run_forward(args, layer_num):
    local_rank = args.local_rank
    rank = torch.distributed.get_rank()
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    world_size = torch.distributed.get_world_size()

    llama_config = config_from_checkpoint('./llama-config/', args.model_size)
    config = llama_config_to_gpt2_config(llama_config)
    overwrite_configs_and_args(config, args)
    args.num_hidden_layers = config.n_layer = layer_num
    print(config)

    print("Creating Dataloader...")
    dataset = DataLoaderForLlama(args)
    trainloader = DataLoader(dataset=dataset,
                            batch_size=args.train_batch_size,
                            shuffle=False)

    print("Creating Model...")
    model = GPTLMHeadModel(config, device='cpu')

    model = construct_fsdp_model(model, device)

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start_iter, end_iter = 10, 20

    print("Profiling...")
    time_list = []
    for ep in range(args.epochs):
        for iter, batch in enumerate(trainloader):
            if iter == end_iter:
                avg_time = sum(time_list) / len(time_list) / args.train_batch_size
                print("Average forward computation time of %d Llama layers (hidden_size=%d) is: %.4f ms / bsz"%(args.num_hidden_layers, args.hidden_size, avg_time))
                return avg_time
            input_ids = batch.to(device)
            torch.cuda.synchronize()
            start.record()
            # model forward
            model_forward(model, input_ids)
            end.record()
            torch.cuda.synchronize()
            iter_time = start.elapsed_time(end)
            if iter >= start_iter:
                time_list.append(iter_time)

def profile(args):
    torch.distributed.init_process_group(backend="nccl")
    
    args.num_hidden_layers = 4
    time_2_layers = run_forward(args, args.num_hidden_layers)
    args.num_hidden_layers = 2
    time_1_layers = run_forward(args, args.num_hidden_layers)
    time_per_layer = (time_2_layers-time_1_layers)/2

    fwd_config_path = './configs/forward_profiling_config.json'
    config = read_json_config(fwd_config_path) if os.path.exists(fwd_config_path) else dict()
    fp16 = '_'+args.mixed_precision
    key = 'fwd_time%s_hidden_%d'%(fp16, args.hidden_size)
    config[key] = time_per_layer
    print('********************')
    print("Average forward computation time of Llama layer (hidden_size=%d) is: %.4f ms / layer / bsz"%(args.hidden_size, time_per_layer))
    write_json_config(config, fwd_config_path)
    print('Already written forward profiling config into env config file %s!\n'%(fwd_config_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--local-rank", type=int, default=-1, help="Local rank.",
    )
    parser.add_argument(
        '--gpu_id', type=int, default=0, help='Id of GPU to run.'
    )
    parser.add_argument(
        "--train_batch_size", type=int, default=32, help="Training batch size"
    )
    parser.add_argument(
        "--model_size", type=str, default='llama-7b', help="Model size.", choices=['llama-7b', 'llama-13b', 'llama-30b']
    )
    parser.add_argument(
        "--overwrite_config", type=int, default=0, help="Whether to overwrite model config"
    )
    parser.add_argument(
        "--hidden_size", type=int, default=768, help="Hidden size of transformer model",
    )
    parser.add_argument(
        "--num_hidden_layers", type=int, default=12, help="Number of layers"
    )
    parser.add_argument(
        "-a",
        "--num_attention_heads",
        type=int,
        default=12,
        help="Number of attention heads",
    )
    parser.add_argument(
        "-s", "--seq_length", type=int, default=128, help="Maximum sequence len"
    )
    parser.add_argument(
        "--vocab_size", type=int, default=30522, help="Total number of vocab"
    )
    parser.add_argument(
        "--dropout_prob", type=float, default=0.1, help="Dropout rate."
    )
    parser.add_argument("--max_predictions_per_seq", type=int, default=20)
    parser.add_argument("-e", "--epochs", type=int,
                        default=10, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=1e-4,
                        help="Learning rate of adam")
    parser.add_argument(
        "--adam_weight_decay", type=float, default=0.01, help="Weight_decay of adam"
    )

    parser.add_argument(
        "--check_loss", type=int, default=0, help="Whether to check model correctness."
    )
    parser.add_argument(
        "--profile", type=int, default=0, help="Whether to profile model GPU memory."
    )
    parser.add_argument(
        "--profile_type", type=str, default='allocated', help="Profile allocated memory or reserved memory.",
        choices = ['allocated', 'reserved'],
    )
    parser.add_argument(
        "--mixed_precision", type=str, default='bf16', help="Mixed precision option.", choices=['fp32', 'fp16', 'bf16'],
    )
    parser.add_argument(
        "--use_flash_attn", type=int, default=0, help="Whether to turn on flash attention."
    )

    args = parser.parse_args()
    set_seed()
    profile(args)
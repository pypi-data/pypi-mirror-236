import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from .dataloader import DataLoaderForCLIP
import argparse
from tqdm import tqdm
import numpy as np
import random
import h5py
import time
import os
import sys
from ..utils import print_peak_memory
from transformers import CLIPModel, CLIPConfig
from ..utils import print_peak_memory
from ..utils import read_json_config, write_json_config
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.api import ShardingStrategy, MixedPrecision, BackwardPrefetch
from .config_utils import *

def set_seed():
    seed = 123
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

def model_forward(model, input_ids, attention_mask, pixel_values):
    loss = model(input_ids=input_ids, 
                 attention_mask=attention_mask, 
                 pixel_values=pixel_values, 
                 return_loss=True).loss
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

def run_forward(args):
    local_rank = args.local_rank
    rank = torch.distributed.get_rank()
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    world_size = torch.distributed.get_world_size()

    print("Creating Model...")
    config = CLIPConfig.from_pretrained(clip_configs(args.model_type))
    if args.overwrite_config:
        config.text_config.num_hidden_layers = args.num_hidden_layers_text
        config.vision_config.num_hidden_layers = args.num_hidden_layers_vision
    # print(obtain_main_config(config))
    
    model = CLIPModel(config)
    
    print("Creating Dataloader...")
    dataset = DataLoaderForCLIP(config)
    trainloader = DataLoader(dataset=dataset,
                            batch_size=args.train_batch_size,
                            shuffle=False)

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
                return avg_time
            input_ids, attention_mask, pixel_values = [t.to(device) for t in batch]
            torch.cuda.synchronize()
            start.record()
            # model forward
            model_forward(model, input_ids, attention_mask, pixel_values)
            end.record()
            torch.cuda.synchronize()
            iter_time = start.elapsed_time(end)
            if iter >= start_iter:
                time_list.append(iter_time)

def profile(args):
    torch.distributed.init_process_group(backend="nccl")
    
    layer_types = ['vision', 'text']
    model_type = args.model_type
    type_num = len(layer_types)
    layernums = [8,16]
    
    def overwrite_layernums(args, layernum_list):
        args.num_hidden_layers_vision, args.num_hidden_layers_text = layernum_list[0], layernum_list[1]
    
    layernum_list = [layernums[0]] * type_num
    overwrite_layernums(args, layernum_list)
    time_base = run_forward(args)
    print("Average forward computation time of", layernum_list, layer_types, " layers (%s) is: %.4f ms / bsz"%(model_type, time_base))
    
    time_per_layer_list = []
    for i in range(type_num):
        layernum_list = [layernums[0]] * type_num
        layernum_list[i] = layernums[1]
        overwrite_layernums(args, layernum_list)
        time_layer_i = run_forward(args)
        print("Average forward computation time of", layernum_list, layer_types, " layers (%s) is: %.4f ms / bsz"%(model_type, time_layer_i))
        time_per_layer_list.append((time_layer_i-time_base)/(layernums[1]-layernums[0]))

    fwd_config_path = './configs/forward_profiling_config.json'
    config = read_json_config(fwd_config_path) if os.path.exists(fwd_config_path) else dict()
    fp16 = '_'+args.mixed_precision
    
    for i in range(type_num):
        key = 'fwd_time%s_%s_%s'%(fp16, model_type, layer_types[i])
        config[key] = time_per_layer_list[i]
        print('********************')
        print("Average forward computation time of %s layer (%s) is: %.4f ms / layer / bsz"%(layer_types[i], model_type, time_per_layer_list[i]))
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
        "--model_type", type=str, default='vit-L-14', help="CLIP model type."
    )
    parser.add_argument(
        "--train_batch_size", type=int, default=32, help="Training batch size"
    )
    parser.add_argument(
        "--overwrite_config", type=int, default=1, help="Whether to overwrite model config"
    )
    parser.add_argument(
        "--hidden_size", type=int, default=768, help="Hidden size of transformer model",
    )
    parser.add_argument(
        "--num_hidden_layers_text", type=int, default=12, help="Number of layers"
    )
    parser.add_argument(
        "--num_hidden_layers_vision", type=int, default=12, help="Number of layers"
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
        "--flash_attn", type=int, default=0, help="Whether to turn on flash attention."
    )

    args = parser.parse_args()
    set_seed()
    profile(args)
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
from ..utils import print_peak_memory, print_param_num
from transformers import CLIPModel, CLIPConfig
from .config_utils import *

torch.backends.cudnn.allow_tf32 = True
torch.backends.cuda.matmul.allow_tf32 = True

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

def train(args):
    cuda_condition = torch.cuda.is_available()
    device = torch.device("cuda:%d"%args.gpu_id if cuda_condition else "cpu")
    rank = args.gpu_id

    print("Creating Model...")
    config = CLIPConfig.from_pretrained(clip_configs(args.model_type))
    if args.overwrite_config:
        config.text_config.num_hidden_layers = args.num_hidden_layers_text
        config.vision_config.num_hidden_layers = args.num_hidden_layers_vision
    print(obtain_main_config(config))
    
    model = CLIPModel(config)
    print_param_num(model)
    model.to(device)

    print("Creating Dataloader...")
    dataset = DataLoaderForCLIP(config)
    trainloader = DataLoader(dataset=dataset,
                            batch_size=args.train_batch_size,
                            shuffle=False)

    optimizer = Adam(model.parameters(), lr=args.lr, weight_decay=args.adam_weight_decay)

    if args.profile:
        print_peak_memory("After creating model", rank, args.profile_type)

    start_iter, end_iter = 5, 20
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
            input_ids, attention_mask, pixel_values = [t.to(device) for t in batch]
            if args.profile and iter <= 2:
                torch.cuda.reset_peak_memory_stats(rank)
                print_peak_memory("\nBefore Forward", rank, args.profile_type)

            loss = model_forward(model, input_ids, attention_mask, pixel_values)

            if args.profile and iter <= 2:
                print_peak_memory("After Forward", rank, args.profile_type)

            loss.backward()

            if args.profile and iter <= 2:
                print_peak_memory("After Backward", rank, args.profile_type)
            
            optimizer.step()

            if args.profile and iter <= 2:
                print_peak_memory("After optimizer_step", rank, args.profile_type)
            
            optimizer.zero_grad()

            end_time = time.time()
            if args.check_loss or args.profile:
                print('[Epoch %d] (Iteration %d): Loss = %.3f'%(ep,iter,loss.item()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

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
        "--overwrite_config", type=int, default=0, help="Whether to overwrite model config"
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
    train(args)
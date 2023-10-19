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
from ..utils import print_peak_memory, print_param_num
from transformers.models.gpt2.configuration_gpt2 import GPT2Config
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

def model_forward(model, input_ids):
    lm_logits = model(input_ids=input_ids).logits
    shift_logits = lm_logits[..., :-1, :].contiguous()
    shift_labels = input_ids[..., 1:].contiguous()
    from flash_attn.losses.cross_entropy import CrossEntropyLoss
    loss_fn = CrossEntropyLoss()
    loss = loss_fn(shift_logits.view(-1, model.config.vocab_size), shift_labels.view(-1).long())
    return loss

def train(args):
    cuda_condition = torch.cuda.is_available()
    device = torch.device("cuda:%d"%args.gpu_id if cuda_condition else "cpu")
    rank = args.gpu_id

    config = gpt_config(args)
    overwrite_configs_and_args(config, args)
    print(config)

    print("Creating Dataloader...")
    dataset = DataLoaderForGPT(args)
    trainloader = DataLoader(dataset=dataset,
                            batch_size=args.train_batch_size,
                            shuffle=False)

    print("Creating Model...")
    model = GPTLMHeadModel(config, device='cpu')
    print_param_num(model)
    
    model.to(device)

    optimizer = Adam(model.parameters(), lr=args.lr, weight_decay=args.adam_weight_decay)

    if args.profile:
        print_peak_memory("After creating model", rank, args.profile_type)

    start_iter, end_iter = 5, 10
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
            if args.profile and iter <= 2:
                torch.cuda.reset_peak_memory_stats(rank)
                print_peak_memory("\nBefore Forward", rank, args.profile_type)

            loss = model_forward(model, input_ids)

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
        "--train_batch_size", type=int, default=32, help="Training batch size"
    )
    parser.add_argument(
        "--model_size", type=str, default='gpt-1.5b', help="Model size.", choices=['gpt-1.5b', 'gpt-2.7b', 'gpt-6.7b']
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
    train(args)
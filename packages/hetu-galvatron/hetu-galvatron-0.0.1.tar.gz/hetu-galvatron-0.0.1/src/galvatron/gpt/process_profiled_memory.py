import sys
import numpy as np
from ..utils import strategy2config, read_json_config, write_json_config, read_allreduce_bandwidth_config, read_p2p_bandwidth_config, estimate_bsz_start_16gpus
import argparse
import re

def match_str(s, pattern):
    match = re.match(pattern, s)
    layernum = int(match.group(1))
    bsz = int(match.group(2))
    rank = int(match.group(3))
    type = match.group(4)
    return layernum, bsz, rank, type

def process_profiled_memory(args):
    world_size = args.gpu_num
    fp16 = '_fp16' if args.use_fp16 else ('_bf16' if args.use_bf16 else '')
    memory_config_path = './configs/memory_profiling_%dgpus_dist%s_hidden%d_head%d_seqlen%d.json'%(world_size, fp16, args.hidden_size, args.num_attention_heads, args.seq_length)
    config = read_json_config(memory_config_path)
    if args.use_fp16:
        memory_config_fp16_path = './configs/memory_profiling_%dgpus_dist_fp16_hidden%d_head%d_seqlen%d.json'%(world_size, args.hidden_size, args.num_attention_heads, args.seq_length)
        config_fp16 = read_json_config(memory_config_fp16_path)
    pattern = r'layernum(\d+)_bsz(\d+)_rank(\d+)_(\w+)'
    format = "layernum%d_bsz%d_rank%d_%s"
    param_result, act_result, param = dict(), dict(), -1
    bsz = 8

    pp_deg, tp_deg = 1, 1
    while True:
        if pp_deg * tp_deg > world_size:
            break
        print(pp_deg, tp_deg)
        strategy = '%d_%d_%d'%(pp_deg,tp_deg,world_size//pp_deg//tp_deg)
        if strategy not in config:
            tp_deg *= 2
            continue
        re = config[strategy]
        if args.use_fp16:
            re_fp16 = config_fp16[strategy]
        layernums = []
        for key, val in re.items():
            # print(key, val)
            layernum, bsz, rank, type = match_str(key, pattern)
            layernums.append(layernum)
        layernums = sorted(list(set(layernums)))
        param_per_layer = (re[format%(layernums[1], bsz, 0, 'ms')] - re[format%(layernums[0], bsz, 0, 'ms')])/(layernums[1]-layernums[0])*pp_deg/4
        act_per_layer_per_sample = (re[format%(layernums[1], bsz, 0, 'act')] - re[format%(layernums[0], bsz, 0, 'act')])/(layernums[1]-layernums[0])*pp_deg/(pp_deg*tp_deg)
        if args.dp_type == 'zero3':
            param_per_layer *= world_size//pp_deg//tp_deg
        if args.use_fp16:
            act_per_layer_per_sample = (re_fp16[format%(layernums[1], bsz, 0, 'act')] - re_fp16[format%(layernums[0], bsz, 0, 'act')])/(layernums[1]-layernums[0])*pp_deg/(pp_deg*tp_deg)
        param = max(param, param_per_layer*tp_deg)
        print(param_per_layer, act_per_layer_per_sample, param)
        param_result[tp_deg] = param_per_layer
        act_result[tp_deg] = act_per_layer_per_sample
        tp_deg *= 2

    print('param:', param)
    # print('param_dict:', param_result)
    print('act_dict:', act_result)

    act_dict_c = dict()
    pp_deg, tp_deg = 1, 1
    act_cpt = -1
    while True:
        if pp_deg * tp_deg > world_size:
            break
        print(pp_deg, tp_deg)
        strategy = '%d_%d_%d_c'%(pp_deg,tp_deg,world_size//pp_deg//tp_deg)
        if strategy not in config:
            tp_deg *= 2
            continue
        re = config[strategy]
        if args.use_fp16:
            re = config_fp16[strategy]
        layernums = []
        for key, val in re.items():
            # print(key, val)
            layernum, bsz, rank, type = match_str(key, pattern)
            layernums.append(layernum)
        layernums = sorted(list(set(layernums)))
        act_per_layer_per_sample = (re[format%(layernums[1], bsz, 0, 'act')] - re[format%(layernums[0], bsz, 0, 'act')])/(layernums[1]-layernums[0])*pp_deg/(pp_deg*tp_deg)
        print(act_per_layer_per_sample)
        act_cpt = max(act_cpt, act_per_layer_per_sample)
        act_dict_c[tp_deg] = act_per_layer_per_sample
        tp_deg *= 2

    print('act_dict_c:', act_dict_c)
    print('act_cpt:', act_cpt)
    act_result['checkpoint'] = act_cpt

    inf=1e6
    other_memory_pp_off, other_memory_pp_on_first, other_memory_pp_on_last = \
        {'model_states': inf, 'activation': inf}, {'model_states': inf, 'activation': inf}, {'model_states': inf, 'activation': inf}
    pp_deg = 1
    while True:
        if pp_deg > world_size:
            break
        tp_deg = 1
        while True:
            if pp_deg * tp_deg > world_size:
                break
            print(pp_deg, tp_deg)
            strategy = '%d_%d_%d'%(pp_deg,tp_deg,world_size//pp_deg//tp_deg)
            if strategy not in config:
                tp_deg *= 2
                continue
            re = config[strategy]
            if args.use_fp16:
                re_fp16 = config_fp16[strategy]
            layernums = []
            for key, val in re.items():
                # print(key, val)
                layernum, bsz, rank, type = match_str(key, pattern)
                layernums.append(layernum)
            layernums = sorted(list(set(layernums)))
            other_ms_first = re[format%(layernums[0], bsz, 0, 'ms')] - layernums[0] / pp_deg * param_result[tp_deg] * 4
            if args.dp_type == 'zero3':
                other_ms_first = (re[format%(layernums[0], bsz, 0, 'ms')] - layernums[0] / pp_deg * param_result[tp_deg] * 4 / (world_size//pp_deg//tp_deg)) * world_size//pp_deg
            other_act_first = re[format%(layernums[0], bsz, 0, 'act')] - layernums[0] / pp_deg * act_result[tp_deg] * (pp_deg*tp_deg)
            other_ms_last = re[format%(layernums[0], bsz, world_size-1, 'ms')] - layernums[0] / pp_deg * param_result[tp_deg] * 4
            if args.dp_type == 'zero3':
                other_ms_last = (re[format%(layernums[0], bsz, world_size-1, 'ms')] - layernums[0] / pp_deg * param_result[tp_deg] * 4 / (world_size//pp_deg//tp_deg)) * world_size//pp_deg
            other_act_last = re[format%(layernums[0], bsz, world_size-1, 'act')] - layernums[0] / pp_deg * act_result[tp_deg] * (pp_deg*tp_deg)
            if args.use_fp16:
                other_act_first = re_fp16[format%(layernums[0], bsz, 0, 'act')] - layernums[0] / pp_deg * act_result[tp_deg] * (pp_deg*tp_deg)
                other_act_last = re_fp16[format%(layernums[0], bsz, world_size-1, 'act')] - layernums[0] / pp_deg * act_result[tp_deg] * (pp_deg*tp_deg)
            print(other_ms_first, other_act_first, other_ms_last, other_act_last)
            if pp_deg == 1:
                other_memory_pp_off['model_states'] = min(other_memory_pp_off['model_states'], other_ms_first)
                other_memory_pp_off['activation'] = min(other_memory_pp_off['activation'], other_act_first)
            else:
                other_memory_pp_on_first['model_states'] = min(other_memory_pp_on_first['model_states'], other_ms_first)
                other_memory_pp_on_first['activation'] = min(other_memory_pp_on_first['activation'], other_act_first / pp_deg)
                other_memory_pp_on_last['model_states'] = min(other_memory_pp_on_last['model_states'], other_ms_last)
                other_memory_pp_on_last['activation'] = min(other_memory_pp_on_last['activation'], other_act_last / pp_deg)
            tp_deg *= 2
        pp_deg *=2

    # other_memory_pp_on_first['activation'] = other_memory_pp_on_last['activation'] = max(other_memory_pp_on_first['activation'], other_memory_pp_on_last['activation'])
    print('other_memory_pp_off:', other_memory_pp_off)
    print('other_memory_pp_on_first:', other_memory_pp_on_first)
    print('other_memory_pp_on_last:', other_memory_pp_on_last)

    if args.use_fp16:
        config_fp16['parameter_size'] = param
        config_fp16['tp_activation_per_bsz_dict'] = act_result
        config_fp16['other_memory_pp_off'] = other_memory_pp_off
        config_fp16['other_memory_pp_on_first'] = other_memory_pp_on_first
        config_fp16['other_memory_pp_on_last'] = other_memory_pp_on_last
        write_json_config(config_fp16, memory_config_fp16_path)
    else:
        config['parameter_size'] = param
        config['tp_activation_per_bsz_dict'] = act_result
        config['other_memory_pp_off'] = other_memory_pp_off
        config['other_memory_pp_on_first'] = other_memory_pp_on_first
        config['other_memory_pp_on_last'] = other_memory_pp_on_last
        write_json_config(config, memory_config_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--layer_num", type=int, default=24, help="Number of layers"
    )
    parser.add_argument(
        "--gpu_num", type=int, default=8, help="Number of GPUs",
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
        "--use_fp16", type=int, default=0, help="Galvatron Run model in fp16 mode."
    )
    parser.add_argument(
        "--use_bf16", type=int, default=0, help="Galvatron Run model in bf16 mode."
    )
    parser.add_argument(
        "--dp_type", type=str, default='ddp', help="Use ddp or zero3 to profile memory.", choices=['ddp', 'zero3']
    )
    args = parser.parse_args()
    process_profiled_memory(args)
import sys
import numpy as np
from ..utils import strategy2config, read_json_config, write_json_config, str2array, array2str
import argparse
import re
from typing import List

def format(layernum, bsz, rank, type):
    if isinstance(layernum, List):
        return "layernum[%s]_bsz%d_rank%d_%s"%(array2str(layernum), bsz, rank, type)
    else:
        return "layernum%d_bsz%d_rank%d_%s"%(layernum, bsz, rank, type)

def match_str(s):
    if '[' in s and ']' in s:
        layernum = str2array(s[s.find('[')+1:s.find(']')])
        s = s[s.find(']')+2:]
        pattern = r'bsz(\d+)_rank(\d+)_(\w+)'
        match = re.match(pattern, s)
        bsz = int(match.group(1))
        rank = int(match.group(2))
        type = match.group(3)
    else:
        pattern = r'layernum(\d+)_bsz(\d+)_rank(\d+)_(\w+)'
        match = re.match(pattern, s)
        layernum = int(match.group(1))
        bsz = int(match.group(2))
        rank = int(match.group(3))
        type = match.group(4)
    return layernum, bsz, rank, type

def get_layernums_bsz(re, layernum_list_flag):
    layernums = []
    for key in re.keys():
        layernum, bsz, _, _ = match_str(key)
        if layernum_list_flag:
            layernums.extend(layernum)
        else:
            layernums.append(layernum)
    layernums = sorted(list(set(layernums)))
    return layernums, bsz

def get_layernum_keys(layernums, layertype, layernum_list_flag, l):
    if len(layernums) == 1:
        layernum_key = [layernums[0]] * layertype if layernum_list_flag else layernums[0]
        return layernum_key, layernum_key
    if layernum_list_flag:
        layernum_key_0, layernum_key_1 = [layernums[0]] * layertype, [layernums[0]] * layertype
        layernum_key_1[l] = layernums[1]
    else:
        layernum_key_0, layernum_key_1 = layernums[0], layernums[1]
    return layernum_key_0, layernum_key_1

def total_memcost(pp_deg, layernum, layertype, layernum_list_flag, per_layer_cost, stage_idx):
    if layernum_list_flag:
        layer_costs = []
        for l in range(layertype):
            layer_costs += [per_layer_cost[l]] * layernum
        
        total_layer_num = layertype * layernum
        avg_layer_num = int(total_layer_num // pp_deg)
        last_layer_num = total_layer_num - avg_layer_num * (pp_deg-1)
        pp_divide = [avg_layer_num] * (pp_deg-1) + [last_layer_num]
        return np.sum(layer_costs[int(np.sum(pp_divide[:stage_idx])):int(np.sum(pp_divide[:stage_idx+1]))])
    else:
        return per_layer_cost * layernum / pp_deg

def process_profiled_memory(args):
    world_size = args.gpu_num
    memory_config_path = './configs/memory_profiling_%dgpus_dist_%s_%s.json'%(world_size, args.mixed_precision, args.model_type)
    config = read_json_config(memory_config_path)

    bsz = 8
    layernum_list_flag = False
    layertype = 1
    
    for key in config['1_1_%s'%world_size].keys():
        layernum, bsz, _, _ = match_str(key)
        if isinstance(layernum, List):
            layertype = len(layernum)
            layernum_list_flag = True
        break
    if layernum_list_flag:
        param_result_list, act_result_list, param_list = [dict() for _ in range(layertype)], [dict() for _ in range(layertype)], [-1]*layertype
    else:
        param_result, act_result, param = dict(), dict(), -1

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
        layernums, bsz = get_layernums_bsz(re, layernum_list_flag)
        for l in range(layertype):
            layernum_key_0, layernum_key_1 = get_layernum_keys(layernums, layertype, layernum_list_flag, l)
            param_per_layer = (re[format(layernum_key_1, bsz, 0, 'ms')] - re[format(layernum_key_0, bsz, 0, 'ms')])/(layernums[1]-layernums[0])*pp_deg/4
            act_per_layer_per_sample = (re[format(layernum_key_1, bsz, 0, 'act')] - re[format(layernum_key_0, bsz, 0, 'act')])/(layernums[1]-layernums[0])*pp_deg/(pp_deg*tp_deg)
            act_per_layer_per_sample *= world_size / bsz
            if args.dp_type == 'zero3':
                param_per_layer *= world_size//pp_deg//tp_deg
            if layernum_list_flag:
                param_result, act_result, param = param_result_list[l], act_result_list[l], param_list[l]
            param = max(param, param_per_layer*tp_deg)
            print(param_per_layer, act_per_layer_per_sample, param)
            param_result[tp_deg] = param_per_layer
            act_result[tp_deg] = act_per_layer_per_sample
            if layernum_list_flag:
                param_result_list[l], act_result_list[l], param_list[l] = param_result, act_result, param
        tp_deg *= 2

    if layernum_list_flag:
        for l in range(layertype):
            print('[layertype %d:]'%l)
            param_result, act_result, param = param_result_list[l], act_result_list[l], param_list[l]
            print('param:', param)
            # print('param_dict:', param_result)
            print('act_dict:', act_result)
    else:
        print('param:', param)
        # print('param_dict:', param_result)
        print('act_dict:', act_result)


    if layernum_list_flag:
        act_dict_c_list, act_cpt_list = [dict() for _ in range(layertype)], [-1]*layertype
    else:
        act_dict_c, act_cpt = dict(), -1
    pp_deg, tp_deg = 1, 1
    while True:
        if pp_deg * tp_deg > world_size:
            break
        print(pp_deg, tp_deg)
        strategy = '%d_%d_%d_c'%(pp_deg,tp_deg,world_size//pp_deg//tp_deg)
        if strategy not in config:
            tp_deg *= 2
            continue
        re = config[strategy]
        layernums, bsz = get_layernums_bsz(re, layernum_list_flag)
        for l in range(layertype):
            layernum_key_0, layernum_key_1 = get_layernum_keys(layernums, layertype, layernum_list_flag, l)
            act_per_layer_per_sample = (re[format(layernum_key_1, bsz, 0, 'act')] - re[format(layernum_key_0, bsz, 0, 'act')])/(layernums[1]-layernums[0])*pp_deg/(pp_deg*tp_deg)
            act_per_layer_per_sample *= world_size / bsz
            print(act_per_layer_per_sample)
            if layernum_list_flag:
                act_dict_c, act_cpt = act_dict_c_list[l], act_cpt_list[l]
            act_cpt = max(act_cpt, act_per_layer_per_sample)
            act_dict_c[tp_deg] = act_per_layer_per_sample
            if layernum_list_flag:
                act_dict_c_list[l], act_cpt_list[l] = act_dict_c, act_cpt
        tp_deg *= 2

    if layernum_list_flag:
        for l in range(layertype):
            print('[layertype %d:]'%l)
            act_dict_c, act_cpt = act_dict_c_list[l], act_cpt_list[l]
            print('act_dict_c:', act_dict_c)
            print('act_cpt:', act_cpt)
            act_result_list[l]['checkpoint'] = act_cpt
    else:
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
            layernums, bsz = get_layernums_bsz(re, layernum_list_flag)
            layernum_key, _ = get_layernum_keys(layernums, layertype, layernum_list_flag, 0)
            
            if layernum_list_flag:
                ms_cost, act_cost = [], []
                for l in range(layertype):
                    ms_cost.append(param_result_list[l][tp_deg]*4)
                    act_cost.append(act_result_list[l][tp_deg])
            else:
                ms_cost = param_result[tp_deg]
                act_cost = act_result[tp_deg]
            
            layer_ms_costs_first = total_memcost(pp_deg, layernums[0], layertype, layernum_list_flag, ms_cost, 0)
            layer_ms_costs_last = total_memcost(pp_deg, layernums[0], layertype, layernum_list_flag, ms_cost, pp_deg-1)
            layer_act_costs_first = total_memcost(pp_deg, layernums[0], layertype, layernum_list_flag, act_cost, 0)
            layer_act_costs_last = total_memcost(pp_deg, layernums[0], layertype, layernum_list_flag, act_cost, pp_deg-1)
            
            other_ms_first = re[format(layernum_key, bsz, 0, 'ms')] - layer_ms_costs_first
            if args.other_dp_type == 'zero3':
                other_ms_first = (re[format(layernum_key, bsz, 0, 'ms')] - layer_ms_costs_first / (world_size//pp_deg//tp_deg)) * world_size//pp_deg
            other_ms_last = re[format(layernum_key, bsz, world_size-1, 'ms')] - layer_ms_costs_last
            if args.other_dp_type == 'zero3':
                other_ms_last = (re[format(layernum_key, bsz, world_size-1, 'ms')] - layer_ms_costs_last / (world_size//pp_deg//tp_deg)) * world_size//pp_deg
            
            other_act_first = re[format(layernum_key, bsz, 0, 'act')] * world_size / bsz  - layer_act_costs_first * (pp_deg*tp_deg) 
            other_act_last = re[format(layernum_key, bsz, world_size-1, 'act')] * world_size / bsz - layer_act_costs_last * (pp_deg*tp_deg) 
            print(other_ms_first, other_act_first, other_ms_last, other_act_last)
            other_act_first = other_act_first if other_act_first > 0 else 0
            other_act_last = other_act_last if other_act_last > 0 else 0
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

    if layernum_list_flag:
        for l in range(layertype):
            if 'layertype_%d'%l not in config.keys():
                config['layertype_%d'%l] = dict()
            config['layertype_%d'%l]['parameter_size'] = param_list[l]
            config['layertype_%d'%l]['tp_activation_per_bsz_dict'] = act_result_list[l]
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
        "--model_type", type=str, default='vit-L-14', help="CLIP model type."
    )
    parser.add_argument(
        "--mixed_precision", type=str, default='fp32', help="Profile memory in mixed precision mode.", choices=['fp32', 'fp16', 'bf16']
    )
    parser.add_argument(
        "--dp_type", type=str, default='ddp', help="Use ddp or zero3 to profile memory.", choices=['ddp', 'zero3']
    )
    parser.add_argument(
        "--other_dp_type", type=str, default='ddp', help="Use ddp or zero3 for embeddings and cls to profile memory.", choices=['ddp', 'zero3']
    )
    args = parser.parse_args()
    process_profiled_memory(args)
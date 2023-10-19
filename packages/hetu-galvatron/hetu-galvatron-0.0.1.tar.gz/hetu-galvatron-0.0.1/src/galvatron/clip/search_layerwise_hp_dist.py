import sys
from ..utils import MemoryCostModelDist, TimeCostModelDist_with_overlap
from ..utils import DpOnModel_dist, print_strategies, form_strategy
import numpy as np
from ..utils import strategy2config, read_json_config, write_json_config, read_allreduce_bandwidth_config, read_p2p_bandwidth_config, estimate_bsz_start_gpunum, array2str
from ..utils import generate_strategies, check_optimal_chunks
import argparse
import copy
from .config_utils import CLIP_config


def read_profiling_configs(gpu_num):
    allreduce_bandwidth_config_path = '../env_configs/allreduce_bandwidth_dist_%d_gpus.json'%gpu_num
    comm_coe_dict = read_allreduce_bandwidth_config(allreduce_bandwidth_config_path, gpu_num=gpu_num)
    overlap_coe_path = '../env_configs/overlap_coefficient.json'
    overlap_coe = read_json_config(overlap_coe_path)['overlap_coe']
    fwd_profiling_path = './configs/forward_profiling_config.json'
    fwd_time = read_json_config(fwd_profiling_path)
    env_config_path = '../env_configs/p2p_bandwidth_dist_%d_gpus.json'%gpu_num
    p2p_comm_coe_dict = None
    # p2p_comm_coe_dict = read_p2p_bandwidth_config(env_config_path, gpu_num=gpu_num)
    return comm_coe_dict, overlap_coe, fwd_time, p2p_comm_coe_dict

def parallelism_optimization(args):
    # # only for memory checking
    # strategies = [[1,1,8,{'fsdp':0}],[1,1,8,{'fsdp':1}],
    #             [1,2,4,{'tp':0,'fsdp':0}],[1,2,4,{'tp':1,'fsdp':0}],[1,2,4,{'tp':0,'fsdp':1}],[1,2,4,{'tp':1,'fsdp':1}],
    #             [1,4,2,{'tp':0,'fsdp':0}],[1,4,2,{'tp':1,'fsdp':0}],[1,4,2,{'tp':0,'fsdp':1}],[1,4,2,{'tp':1,'fsdp':1}],
    #             [1,8,1,{}],
    #             [2,1,4,{'fsdp':0}],[2,1,4,{'fsdp':1}],
    #             [2,2,2,{'tp':0,'fsdp':0}],[2,2,2,{'tp':1,'fsdp':0}],[2,2,2,{'tp':0,'fsdp':1}],[2,2,2,{'tp':1,'fsdp':1}],
    #             [2,4,1,{}],
    #             [4,1,2,{'fsdp':0}],[4,1,2,{'fsdp':1}],
    #             [4,2,1,{}],
    #             [8,1,1,{}]]

    assert(not(args.disable_sdp and args.disable_dp))
    strategies = generate_strategies(args.gpu_num, args.type)

    strategies_new = []
    for s in strategies:
        if args.disable_tp_consec and 'tp' in s[-1] and s[-1]['tp'] == 0:
            continue
        if args.disable_sdp and 'fsdp' in s[-1] and s[-1]['fsdp'] == 1:
            continue
        if args.disable_dp and not ('fsdp' in s[-1] and s[-1]['fsdp'] == 1):
            continue
        if s[1] >= 8:
            continue
        if s[0] >= 8:
            continue
        strategies_new.append(s)
    strategies = strategies_new

    if args.checkpoint == 1:
        strategies_cpt = []
        for s in strategies:
            s_cpt = copy.deepcopy(s)
            s_cpt[-1]['cpt']=1
            strategies_cpt.append(s_cpt)
        strategies += strategies_cpt
        # strategies = strategies_cpt

    # Load profiling configs
    gpu_num = args.gpu_num
    comm_coe_dict, overlap_coe, fwd_time, p2p_comm_coe_dict = read_profiling_configs(gpu_num)
    config = CLIP_config(args.model_type)
    layer_types = ['vision', 'text']
    type_nums = len(layer_types)
    layer_num_list, hidden_size_list, seq_len_list, fwd_time_list = [], [], [], []
    for i in range(type_nums):
        layer_num_list.append(config[layer_types[i]]['layer_num'])
        hidden_size_list.append(config[layer_types[i]]['hidden_size'])
        seq_len_list.append(config[layer_types[i]]['seq_len'])
        fwd_time_list.append(fwd_time['fwd_time_%s_%s_%s'%(args.mixed_precision,args.model_type, layer_types[i])])

    print('================================================================================')
    print('------- Model configs -------')
    print('Layer types:', layer_types)
    print('Layer_num:', layer_num_list)
    print('Hidden_size:', hidden_size_list)
    print('Seq_len:', seq_len_list)
    print('================================================================================')
    print('--- Optimization configs ----')
    print('Memory_constraint: %d GB'%args.memory_constraint)
    print('Optimization type:', args.type)
    print('================================================================================')
    print('---- Environment configs ----')
    print('Allreduce comm_coe dict (ms/MB):', comm_coe_dict)
    print('P2P comm_coe dict (ms/MB):', p2p_comm_coe_dict)
    print('Overlap coefficient:', overlap_coe)
    print('--- Model forward configs ---')
    print('Forward computation time:', fwd_time_list)
    print('================================================================================')

    def optimal_chunk_func(local_bsz, strategy):
        if strategy[0] == 1:
            return 1
        local_bsz = local_bsz // strategy[1]
        re = np.ceil(local_bsz / 4)
        re = 1 if re == 0 else re
        re = min(8,re)
        return int(re)

    microbatch = True
    
    memcost_model_args_list, timecost_model_args_list = [], []
    
    memory_config_path = './configs/memory_profiling_%dgpus_dist_%s_%s.json'%(8, args.mixed_precision, args.model_type)
    mem_config = read_json_config(memory_config_path)
    other_memory_pp_off = mem_config['other_memory_pp_off']
    other_memory_pp_on_first, other_memory_pp_on_last = mem_config['other_memory_pp_on_first'], mem_config['other_memory_pp_on_last']
    other_memory_pp_on = {'first_stage':other_memory_pp_on_first, 'last_stage':other_memory_pp_on_last}
    print(other_memory_pp_off)
    print(other_memory_pp_on)
    for i in range(type_nums):
        layer_mem_config = mem_config['layertype_%d'%i]
        parameter_size = layer_mem_config['parameter_size']
        tp_activation_per_bsz_dict = layer_mem_config['tp_activation_per_bsz_dict'].copy()
        for key, val in layer_mem_config['tp_activation_per_bsz_dict'].items():
            if len(key) < 5:
                tp_activation_per_bsz_dict[int(key)] = val
        print('[Layertype %s]'%layer_types[i])
        print(parameter_size)
        print(tp_activation_per_bsz_dict)

        memcost_model_args = {  'parameter_size': parameter_size,
                                'tp_activation_per_bsz_dict': tp_activation_per_bsz_dict,
                                'other_memory_pp_off': other_memory_pp_off,
                                'other_memory_pp_on': other_memory_pp_on,
                                'microbatch': microbatch,
                                'optimal_chunk_func': optimal_chunk_func,
                                'model_type': 'gpt',
                                'checkpoint':args.checkpoint,
                                'use_zero2_for_dp':args.use_zero2_for_dp,
                                'use_zero3_for_embed':args.use_zero3_for_embed,
                                'mixed_precision':False if args.mixed_precision == 'fp32' else True,
                                'pipeline_type': args.pipeline_type}
        timecost_model_args = { 
                                'parameter_size': parameter_size,
                                'microbatch': microbatch,
                                'optimal_chunk_func': optimal_chunk_func,
                                'sequence_length': seq_len_list[i],
                                'hidden_size': hidden_size_list[i],
                                'forward_computation_time': fwd_time_list[i],
                                'bct_fct_coe': 2,
                                'extra_overhead': 0,
                                'comm_coe_dict': comm_coe_dict,
                                'dp_overlap_coe': overlap_coe,
                                'bct_overlap_coe': overlap_coe,
                                'p2p_comm_coe_dict': p2p_comm_coe_dict,
                                'layer_num': layer_num_list[i],
                                'use_zero2_for_dp':args.use_zero2_for_dp,
                                'mixed_precision':False if args.mixed_precision == 'fp32' else True}
        memcost_model_args_list.append(memcost_model_args)
        timecost_model_args_list.append(timecost_model_args)

    def pp_stage_divide_greedy(memcost_model_args, layer_num, pp_deg, bsz, strategies):
        assert(len(memcost_model_args)==len(layer_num))
        if pp_deg == 1:
            return [np.sum(layer_num)], None
        layer_type_num = len(layer_num)
        layer_min_memcost = []
        strategies = list(filter(lambda s: s[0] == pp_deg, strategies))
        if len(strategies)==0:
            return None, None
        for i in range(layer_type_num):
            memcosts = [MemoryCostModelDist(strategy, global_batch_size=bsz, **memcost_model_args[i]).get_memory_cost()['enc_total'] for strategy in strategies]
            layer_min_memcost.append(np.min(memcosts))
        other_cost = MemoryCostModelDist(strategies[0], global_batch_size=bsz, **memcost_model_args[0]).get_memory_cost()['other']
        #print(layer_min_memcost, other_cost)
        min_memcost_all_layers = []
        for i in range(layer_type_num):
            min_memcost_all_layers += [layer_min_memcost[i]]*layer_num[i]
        #print(min_memcost_all_layers)
        avg_mem_cost = (np.sum(min_memcost_all_layers)+np.sum(other_cost))/pp_deg
        #print('Avg memcost:', avg_mem_cost)

        pp_divide = [0]*pp_deg
        mem_cost_per_stage = other_cost.copy()
        idx = len(min_memcost_all_layers)-1
        for i in range(pp_deg-1,-1,-1):
            while True:
                if idx < 0:
                    break
                if i > 0 and avg_mem_cost - mem_cost_per_stage[i] < 0.5 * min_memcost_all_layers[idx]:
                    break
                else:
                    mem_cost_per_stage[i]+=min_memcost_all_layers[idx]
                    idx-=1
                    pp_divide[i]+=1
        # print(pp_divide)

        # Avoid too much memory cost on previous stages
        for i in range(pp_deg-1):
            left, right = int(np.sum(pp_divide[:i])), int(np.sum(pp_divide[:i+1]))
            mem_cost_cur_stage = np.sum(min_memcost_all_layers[left:right]) + other_cost[i]
            while mem_cost_cur_stage > avg_mem_cost * 1.3:
                pp_divide[i] -= 1
                pp_divide[i+1] += 1
                right -= 1
                mem_cost_cur_stage -= min_memcost_all_layers[right]

        # Avoid no layers on previous stages
        for i in range(pp_deg-1):
            while pp_divide[i] <= 0:
                pp_divide[i] += 1
                pp_divide[i+1] -= 1

        # Avoid no layers on last stage
        for i in range(pp_deg-1, 0, -1):
            while pp_divide[i] <= 0:
                pp_divide[i] += 1
                pp_divide[i-1] -= 1
        
        mem_cost_per_stage_adjusted = other_cost.copy()
        # print(pp_divide)
        # print(other_cost, avg_mem_cost)
        for i in range(pp_deg):
            left, right = int(np.sum(pp_divide[:i])), int(np.sum(pp_divide[:i+1]))
            mem_cost_per_stage_adjusted[i] +=  np.sum(min_memcost_all_layers[left:right])
        # print(mem_cost_per_stage,mem_cost_per_stage_adjusted)
        return pp_divide, mem_cost_per_stage_adjusted

    def get_pp_stages_for_all_bsz():
        bszs = list(range(8, 10240, 8))
        pp_stage_dict_for_bsz = dict()
        for bsz in bszs:
            pp_stage_dict = dict()
            pp_deg_list = sorted(list(set([s[0] for s in strategies])))
            for pp_deg in pp_deg_list:
                pp_divide, mem_cost_per_stage = pp_stage_divide_greedy(memcost_model_args_list, layer_num_list, pp_deg, bsz, strategies)
                #print(bsz, pp_deg, pp_divide, mem_cost_per_stage)
                pp_stage_dict[pp_deg] = pp_divide
            pp_stage_dict_for_bsz[bsz] = pp_stage_dict
        return pp_stage_dict_for_bsz

    search_history = dict()
    def search(max_mem):
        bsz_scale = 32
        bsz_scale = 32 if args.type == 'dp+tp' and bsz_scale < 32 else bsz_scale
        bsz_start = bsz_scale if args.search_from_min_bsz else estimate_bsz_start(bsz_scale)
        print('Searching batch_size start from: %d, batch_size scale: %d'%(bsz_start, bsz_scale))
        print("----Searching with max memory %d MB----"%max_mem)
        results = dict()
        max_throughput, optimal_bsz, max_bsz = -1, -1, -1
        for bsz in range(bsz_start, 10240, bsz_scale):
            pp_stage_dict = pp_stage_dict_for_bsz[bsz]
            print('bsz=%d'%bsz, pp_stage_dict)
            dp_on_model = DpOnModel_dist(strategies, 
                                    MemoryCostModelDist, 
                                    TimeCostModelDist_with_overlap, 
                                    memcost_model_args=memcost_model_args_list,
                                    timecost_model_args=timecost_model_args_list,
                                    max_mem=max_mem,
                                    layer_num =layer_num_list,
                                    multi_layer_type = True,
                                    pp_stage_dict = pp_stage_dict,
                                    search_history=search_history,
                                    comm_coe_dict=comm_coe_dict,
                                    gpu_num=gpu_num,
                                    pipeline_type=args.pipeline_type)
            
            if args.settle_bsz > 0:
                bsz = args.settle_bsz
            print("****Testing with bsz=", bsz, "****")
            
            chunk_dict = check_optimal_chunks(args.gpu_num, strategies, optimal_chunk_func, bsz)
            print('Chunk_dict for bsz %d: '%bsz, chunk_dict)
            
            min_cost, min_res_list, min_pp_deg, mem_remain, mem_cost = dp_on_model.fit(bsz)
            throughput = bsz / min_cost
            print(f"[Optimal pp_deg={min_pp_deg}] Minimized timecost={min_cost} Memory remaining={mem_remain} Memory cost={mem_cost}")
            print(f"Max throughput={throughput} samples/s")
            print_strategies(min_res_list)
            results[bsz] = {'min_cost': min_cost, 'min_res_list': min_res_list, 'min_pp_deg': min_pp_deg, 
                            'mem_remain': mem_remain, 'mem_cost': mem_cost, 'throughput': throughput}
            if throughput > max_throughput:
                max_throughput = throughput
                optimal_bsz = bsz
            if min_pp_deg == -1 and min_res_list is None:
                break
            max_bsz = bsz
            if args.settle_bsz > 0:
                break

        print('\nFinal results of max memory %d MB:'%max_mem)
        re = results[optimal_bsz]
        print(f"Optimal bsz = {optimal_bsz} Max throughput={re['throughput']} samples/s")
        print(f"pp_deg={re['min_pp_deg']} Minimized timecost={re['min_cost']} Memory remaining={re['mem_remain']} Memory cost={re['mem_cost']}")
        print_strategies(re['min_res_list'])

        if re['min_pp_deg'] > 0 and re['min_res_list'] is not None:
            result_strategy = []
            if isinstance(re['min_res_list'],list):
                for l in re['min_res_list']:
                    result_strategy += l
            else:
                result_strategy = re['min_res_list']
            config = strategy2config(result_strategy)
            config['global_bsz'] = optimal_bsz
            config['chunks'] = max([int(optimal_chunk_func(optimal_bsz//s[2],s)) for s in result_strategy]) if config['pp_deg'] > 1 else 1
            config['pp_division'] = array2str(pp_stage_dict_for_bsz[optimal_bsz][config['pp_deg']])
            cpt = '_cpt' if args.checkpoint else ''
            if args.checkpoint:
                config['checkpoint'] = array2str([1 if 'cpt' in s[-1] and s[-1]['cpt'] else 0 for s in result_strategy])
            settle_bsz = '_bsz%d'%args.settle_bsz if args.settle_bsz > 0 else ''
            disable_sdp = '_sdpoff' if args.disable_sdp else ('_dpoff' if args.disable_dp else '')
            zero2 = '_zero2' if args.use_zero2_for_dp else ''
            pp_type = '_1f1b' if args.pipeline_type == 'pipedream_flush' else ''
            config['pipeline_type'] = args.pipeline_type
            file_name = './configs/galvatron_config_%dgpus_%s_%dG_%s%s%s%s%s%s_%s.json'%(gpu_num,args.model_type,max_mem//1024,args.type,cpt,pp_type,settle_bsz,disable_sdp,zero2,args.mixed_precision)
            write_json_config(config, file_name)
            print('Already written optimized parallelism config into galvatron config file %s!'%(file_name))

        if max_bsz > -1 and max_bsz != optimal_bsz:
            re = results[max_bsz]
            print(f"\nMax bsz = {max_bsz} Max throughput={re['throughput']} samples/s")
            print(f"pp_deg={re['min_pp_deg']} Minimized timecost={re['min_cost']} Memory remaining={re['mem_remain']} Memory cost={re['mem_cost']}")
            print_strategies(re['min_res_list'])
        print("-----------------------------------------")


    # Check cost model
    def check_cost_model():
        bsz = 32
        for i in range(type_nums):
            memcost_model_args, timecost_model_args, layer_num = memcost_model_args_list[i], timecost_model_args_list[i], layer_num_list[i]
            for strategy in strategies:
                re = MemoryCostModelDist(strategy, global_batch_size=bsz, **memcost_model_args).get_memory_cost()
                print(form_strategy(strategy), re['enc_total'], re['other'][0], re['other'][-1], re['enc_total']*layer_num/strategy[0]+re['other'][0], re['enc_total']*layer_num/strategy[0]+re['other'][-1])
            print()
            for strategy in strategies:
                re = TimeCostModelDist_with_overlap(strategy, global_batch_size=bsz, **timecost_model_args).gen_result()
                print(form_strategy(strategy), re*layer_num)
            print()

    def estimate_bsz_start(scale):
        def estimate_strategy_max_bsz(s):
            max_bsz = 0
            scale_ = 32 if s[0][0] == 1 and scale < 32 else scale
            for bsz in range(scale_, 10240, scale_):
                pp_stage_dict = pp_stage_dict_for_bsz[bsz]
                dp_on_model = DpOnModel_dist(s, MemoryCostModelDist, TimeCostModelDist_with_overlap, 
                                        memcost_model_args_list, timecost_model_args_list,
                                        max_mem=max_mem, layer_num=layer_num_list, 
                                        multi_layer_type = True, pp_stage_dict = pp_stage_dict,
                                        comm_coe_dict=comm_coe_dict, gpu_num=gpu_num)
                min_cost, min_res_list, min_pp_deg, mem_remain, mem_cost = dp_on_model.fit(bsz, False)
                if min_pp_deg == -1:
                    max_bsz = bsz - scale_
                    break
            return max_bsz
        bsz_start = estimate_bsz_start_gpunum(args.type,scale,estimate_strategy_max_bsz,gpu_num)
        return bsz_start

    check_cost_model()
    pp_stage_dict_for_bsz = get_pp_stages_for_all_bsz()
    # print(pp_stage_dict_for_bsz)
    mem_list = [8, 12, 16, 20]
    if args.memory_constraint > 0:
        mem_list = [args.memory_constraint]
    mem_list = [mem * 1024 for mem in mem_list]
    for max_mem in mem_list:
        search(max_mem)
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--layer_num", type=int, default=24, help="Number of layers"
    )
    parser.add_argument(
        "--gpu_num", type=int, default=32, help="Number of GPUs",
    )
    parser.add_argument(
        "--memory_constraint", type=int, default=8, help="Memory constraint of Galvatron",
    )
    parser.add_argument(
        "--type", type=str, default='full', help="Galvatron parallelism optimization type.", choices=['full','dp+tp','dp+pp'],
    )
    parser.add_argument(
        "--search_from_min_bsz", type=int, default=0, help="If 0, start searching from a recommended bsz to accelerate optimization.",
    )
    parser.add_argument(
        "--model_type", type=str, default='vit-L-14', help="CLIP model type."
    )
    parser.add_argument(
        "--checkpoint", type=int, default=0, help="Enable checkpoint or not."
    )
    parser.add_argument(
        "--settle_bsz", type=int, default=-1, help="Settle batch size or not."
    )
    parser.add_argument(
        "--disable_sdp", type=int, default=0, help="Whether to disable sdp."
    )
    parser.add_argument(
        "--disable_dp", type=int, default=0, help="Whether to disable dp."
    )
    parser.add_argument(
        "--disable_tp_consec", type=int, default=0, help="Whether to disable tp_consec."
    )
    parser.add_argument(
        "--use_zero2_for_dp", type=int, default=0, help="Whether to use_zero2_for_dp."
    )
    parser.add_argument(
        "--use_zero3_for_embed", type=int, default=0, help="Whether to use zero3 for embedding and cls layers."
    )
    parser.add_argument(
        "--mixed_precision", type=str, default='bf16', help="Mixed precision option.", choices=['fp32', 'fp16', 'bf16'],
    )
    parser.add_argument(
        "--pipeline_type", type=str, default="gpipe", help="Galvatron pipeline type", choices=["gpipe","pipedream_flush"],
    )
    args = parser.parse_args()
    parallelism_optimization(args)
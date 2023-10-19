import os
import sys
import torch
from torch import nn
import numpy as np
from ..utils import gen_groups_dist, modules_to_devices, wrap_modules_data_parallel, wrap_modules_relocation, wrap_data_parallel, wrap_modules_checkpoint
from ..utils import read_json_config, config2strategy, str2array
from ..pipeline import PipelineParallel, PipeSequential
from transformers.models.clip.modeling_clip import CLIPEncoderLayer

def get_chunks(args):
    if args.chunks == -1:
        args.chunks = 1
        if args.pp_deg > 1:
            world_size = torch.distributed.get_world_size()
            max_dp_deg = world_size // args.pp_deg
            local_bsz = args.global_train_batch_size // max_dp_deg
            optimal_micro_bsz = np.ceil(local_bsz / 4)
            optimal_micro_bsz = 1 if optimal_micro_bsz == 0 else optimal_micro_bsz
            args.chunks = int(optimal_micro_bsz)
    return args.chunks

def overwrite_megatron_args(config, args):
    args.fp16 = True if args.mixed_precision == 'fp16' else False
    args.bf16 = True if args.mixed_precision == 'bf16' else False
    args.use_cpu_initialization = True

def get_pp_ranks_enc(pp_divide):
    pp_ranks_enc = []
    pp_deg = len(pp_divide)
    for i in range(pp_deg):
        pp_ranks_enc += [i]*pp_divide[i]
    return pp_ranks_enc

def get_hybrid_parallel_configs(args):
    local_rank = args.local_rank
    world_size = torch.distributed.get_world_size()
    total_layer_num = args.num_hidden_layers_vision + args.num_hidden_layers_text
    config_type = 'JSON' if args.galvatron_config_path not in [None,'None'] else 'PYTHON' if args.apply_strategy else 'GLOBAL'
    if local_rank == 0:
        print('======================== Galvatron Parallel Config =============================')
        print('Galvatron parallel config mode: [%s config mode]'%config_type)
    if config_type == 'GLOBAL':
        pp_deg = args.pp_deg
        tp_sizes_enc = [args.global_tp_deg] * total_layer_num if args.global_tp_deg > 0 else [1]*total_layer_num
        tp_consecutive_flags = [args.global_tp_consec] * total_layer_num if args.global_tp_consec in [0, 1] else [1]*total_layer_num
        dp_types_enc = total_layer_num * [args.fsdp]
        checkpoint_flags_enc = [args.global_checkpoint] * total_layer_num
    elif config_type == 'JSON':
        galvatron_config = read_json_config(args.galvatron_config_path)
        pp_deg, tp_sizes_enc, tp_consecutive_flags, dp_types_enc = config2strategy(galvatron_config)
        bsz, chunks = galvatron_config['global_bsz'], galvatron_config['chunks']
        if 'checkpoint' in galvatron_config.keys():
            checkpoint_flags_enc = str2array(galvatron_config['checkpoint'])
        else:
            checkpoint_flags_enc = [0] * len(tp_sizes_enc)
        pp_divide = str2array(galvatron_config['pp_division'])
        config_source = 'Galvatron JSON config %s'%args.galvatron_config_path
        pp_ranks_enc = get_pp_ranks_enc(pp_divide)
        if local_rank == 0 and (total_layer_num != len(tp_sizes_enc) or args.chunks != chunks or args.global_train_batch_size != bsz):
            print('[Notice] The following hyper-parameters will be overwritten by Galvatron %s config:'%config_type)
            if args.global_train_batch_size != bsz:
                print('   global_batch_size =', bsz)
            if args.chunks != chunks:
                print('   chunks =', chunks)
            if total_layer_num != len(tp_sizes_enc):
                assert(False, 'Layer_num in json config does not match layer_num in the model!')
        args.global_train_batch_size = bsz
        args.chunks = chunks
    
    if config_type == 'GLOBAL':
        avg_layer_num = int(total_layer_num // pp_deg)
        last_layer_num = total_layer_num - avg_layer_num * (pp_deg-1)
        pp_divide = [avg_layer_num] * (pp_deg-1) + [last_layer_num]
        pp_ranks_enc = get_pp_ranks_enc(pp_divide)

    assert args.global_train_batch_size % (world_size//pp_deg) == 0, 'global_train_batch_size should be multiple of world_size//pp_deg!'
    if local_rank == 0:
        if config_type == 'GLOBAL':
            print('[GLOBAL config mode] Loaded global hybrid parallel strategy:')
            dp_type = 'sdp' if args.fsdp else 'dp'
            tp_deg, tp_consec = tp_sizes_enc[0], tp_consecutive_flags[0]
            dp_deg = world_size//args.global_tp_deg//args.pp_deg
            print('   global_batch_size: %d, chunks: %d'%(args.global_train_batch_size, get_chunks(args)))
            print('   pp_deg: %d, tp_deg: %d, %s_deg: %d, tp_consecutive_flag: %d, checkpoint_flag: %d'%(pp_deg, tp_deg, dp_type, dp_deg, tp_consec, args.global_checkpoint))
            print('   pp_division:\t\t', pp_divide)
            print('   pp_ranks:\t\t', pp_ranks_enc)
        else:
            print('[%s config mode] Loaded hybrid parallel config from %s:'%(config_type, config_source))
            print('   global_batch_size: %d, chunks: %d, pp_deg: %d'%(args.global_train_batch_size, args.chunks, pp_deg))
            print('   tp_sizes_enc:\t', tp_sizes_enc)
            print('   tp_consecutive_flags:', tp_consecutive_flags)
            print('   dp_types_enc:\t', dp_types_enc)
            print('   checkpoint_flags:\t', checkpoint_flags_enc)
            print('   pp_division:\t\t', pp_divide)
            print('   pp_ranks:\t\t', pp_ranks_enc)
        print('================================================================================')
    hybrid_parallel_configs =   {'pp_deg':pp_deg,
                                'tp_sizes_enc':tp_sizes_enc,
                                'tp_consecutive_flags':tp_consecutive_flags,
                                'dp_types_enc':dp_types_enc,
                                'pp_ranks_enc':pp_ranks_enc,
                                'checkpoint_flags_enc':checkpoint_flags_enc}
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    clip_model, config, args, hp_configs = model, model_config, training_args, hybrid_parallel_configs
    pp_deg, tp_sizes_enc, tp_consecutive_flags, dp_types_enc, pp_ranks_enc, checkpoint_flags_enc = \
        hp_configs['pp_deg'], hp_configs['tp_sizes_enc'], hp_configs['tp_consecutive_flags'], hp_configs['dp_types_enc'], hp_configs['pp_ranks_enc'], hp_configs['checkpoint_flags_enc']
    total_layer_num = config.vision_config.num_hidden_layers + config.text_config.num_hidden_layers
    assert total_layer_num == len(tp_sizes_enc)
    assert total_layer_num == len(dp_types_enc) 
    assert total_layer_num == len(pp_ranks_enc)
    assert total_layer_num == len(checkpoint_flags_enc)
    world_size = torch.distributed.get_world_size()
    for tp_size in tp_sizes_enc:
        assert tp_size <= world_size//pp_deg and (world_size//pp_deg) % tp_size == 0 and tp_size >= 1, 'Wrong tp_size!'
    for dp_type in dp_types_enc:
        assert dp_type == 0 or dp_type == 1 or dp_type is None, 'Wrong dp_type!'
    for pp_rank in pp_ranks_enc:
        assert pp_rank >= 0 and pp_rank <= pp_deg - 1, 'Wrong pp_rank!'

    # [Step 0] Construct sizes & groups
    # Construct tp_sizes / dp_types / pp_stages for whole model
    tp_sizes_whole_model = [1, 1] + tp_sizes_enc + [1, 1, 1]
    dp_types_whole_model = [0, 0] + dp_types_enc + [0, 0, 0]
    pp_ranks_whole_model = [0, 0] + pp_ranks_enc + [pp_deg-1, pp_deg-1, pp_deg-1]
    tp_consecutive_whole_model = [1, 1] + tp_consecutive_flags + [1, 1, 1]
    # Construct pp_group / tp_groups / dp_groups / allgather_groups / slice_funcs
    pp_group, tp_groups_whole_model, dp_groups_whole_model, allgather_groups_whole_model, slice_funcs_whole_model = gen_groups_dist(tp_sizes_whole_model, pp_deg, tp_consecutive_whole_model, show_rank = 0)
    tp_groups_enc = tp_groups_whole_model[2:-3]

    # # [Step 1] Construct Tensor Parallel Block based on tp_groups
    from .CLIPModel_tensor_parallel import CLIPAttention_tp, CLIPMLP_tp, overwrite_vision_configs, overwrite_text_configs
    overwrite_vision_configs(args, config)
    for i in range(config.vision_config.num_hidden_layers):
        layer = clip_model.vision_model.encoder.layers[i]
        setattr(layer, 'self_attn', CLIPAttention_tp(config, 'vision', tp_group = tp_groups_enc[i]))
        setattr(layer, 'mlp', CLIPMLP_tp(config, tp_group = tp_groups_enc[i]))
    overwrite_text_configs(args, config)
    for i in range(config.text_config.num_hidden_layers):
        layer = clip_model.text_model.encoder.layers[i]
        idx = i+config.vision_config.num_hidden_layers
        setattr(layer, 'self_attn', CLIPAttention_tp(config, 'text', tp_group = tp_groups_enc[idx]))
        setattr(layer, 'mlp', CLIPMLP_tp(config, tp_group = tp_groups_enc[idx]))

    # [Step 2] Construct Sequantial modules
    from .CLIPModel_pipeline import construct_sequential_model
    model = construct_sequential_model(clip_model, config)

    # [Step 3] Wrap Relocation modules if necessary
    model = wrap_modules_relocation(model, allgather_groups_whole_model, slice_funcs_whole_model)

    # [Step 4] Construct Pipeline Module and place the layers on corresponding devices
    mixed_precision = {'fp32': torch.float, 'fp16': torch.float16, 'bf16': torch.bfloat16}[args.mixed_precision]
    text_seq_len, img_seq_len = config.text_config.max_position_embeddings, (config.vision_config.image_size // config.vision_config.patch_size) ** 2 + 1
    text_hidden_size, img_hidden_size = config.text_config.hidden_size, config.vision_config.hidden_size
    layer_output_shape = [[-1, text_seq_len], [-1, text_seq_len], [-1, text_seq_len, text_hidden_size], [-1, 1, text_seq_len, text_seq_len], [-1, img_seq_len, img_hidden_size]]
    layer_output_dtype = [torch.long] + [mixed_precision] * 4
    layer_output_tensor_shapes = [None, None] + [layer_output_shape] * total_layer_num + [None] * 3
    layer_output_tensor_dtypes = [None, None] + [layer_output_dtype] * total_layer_num + [None] * 3
    layer_dp_sizes = [world_size // pp_deg // tp_size for tp_size in tp_sizes_whole_model]
    hp_model = PipelineParallel(
                model = model, 
                model_ranks = pp_ranks_whole_model, 
                layer_output_tensor_shapes = layer_output_tensor_shapes, 
                layer_output_tensor_dtypes = layer_output_tensor_dtypes,
                layer_dp_sizes = layer_dp_sizes, 
                chunks=args.chunks, 
                process_group = pp_group.ranks, 
                nproc_per_node=8,
                require_loss=False,
                info=False)

    # [Step 5] Wrap Data Parallel modules based on dp_types & dp_groups
    module_types = ['embed_vis', 'embed_text'] + ['clip_vis_enc']*config.vision_config.num_hidden_layers + ['clip_text_enc']*config.text_config.num_hidden_layers + ['vis_post', 'text_post', 'cls']
    hp_model.wrap_pipeline_modules_data_parallel(dp_types_whole_model, dp_groups_whole_model, module_types=module_types, mixed_precision=mixed_precision, wrap_block_name=[CLIPEncoderLayer])
    
    checkpoint_flags_whole_model = [0, 0] + checkpoint_flags_enc + [0, 0, 0]
    hp_model.wrap_pipeline_modules_checkpoint(checkpoint_flags_whole_model, wrap_block_name=[CLIPEncoderLayer])
    return hp_model
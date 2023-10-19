import os
from transformers import GPT2Config

def gpt_config(args):
    import json
    with open(os.path.join(os.path.dirname(__file__), 'gpt-config', '%s.json'%args.model_size)) as f:
        params = json.load(f)
    return GPT2Config(**params)

def overwrite_configs_and_args(config, args):
    overwrite_config = {'use_cache': False,
                        'use_flash_attn': args.use_flash_attn,
                        'fused_bias_fc': True,
                        'sequence_parallel': False}
    for key, val in overwrite_config.items():
        setattr(config, key, val)
    
    if args.overwrite_config:
        overwrite_config = {'hidden_size': args.hidden_size,
                            'max_position_embeddings': args.seq_length,
                            'num_hidden_layers': args.num_hidden_layers,
                            'vocab_size': args.vocab_size}
        for key, val in overwrite_config.items():
            setattr(config, key, val)
    else:
        args.hidden_size = config.hidden_size
        args.seq_length = config.max_position_embeddings
        args.max_position_embeddings = config.max_position_embeddings
        args.num_hidden_layers = config.num_hidden_layers
        args.vocab_size = config.vocab_size
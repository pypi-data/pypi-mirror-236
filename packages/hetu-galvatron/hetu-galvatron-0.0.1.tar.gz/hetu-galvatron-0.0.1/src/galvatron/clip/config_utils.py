
def clip_configs(model_type):
    return {
        'vit-B-16': './clip_hf_configs/CLIP-ViT-B-16.json',
        'vit-L-14': './clip_hf_configs/CLIP-ViT-L-14-laion2B-s32B-b82K.json',
        'vit-H-14': './clip_hf_configs/CLIP-ViT-H-14-laion2B-s32B-b79K.json',
        'vit-g-14': './clip_hf_configs/CLIP-ViT-g-14-laion2B-s12B-b42K.json',
        'vit-bigG-14': './clip_hf_configs/CLIP-ViT-bigG-14-laion2B-39B-b160k.json',
    }[model_type]

def obtain_main_config(config):
    main_config={
        'embed_dim': config.projection_dim,
        'vision_cfg': {
            'layer_num': config.vision_config.num_hidden_layers,
            'hidden_size': config.vision_config.hidden_size,
            'head_num': config.vision_config.num_attention_heads,
            'image_size': config.vision_config.image_size,
            'patch_size': config.vision_config.patch_size,
        },
        'text_cfg': {
            'layer_num': config.text_config.num_hidden_layers,
            'hidden_size': config.text_config.hidden_size,
            'head_num': config.text_config.num_attention_heads,
            'seq_len': config.text_config.max_position_embeddings,
            'vocab_size': config.text_config.vocab_size,
        }
    }
    return main_config

def CLIP_config(model_type):
    return {
        'vit-B-16': {
            'vision': {
                'hidden_size': 768,
                'seq_len': 197,
                'layer_num': 12,
            },
            'text': {
                'hidden_size': 512,
                'seq_len': 77,
                'layer_num': 12,
            }
        },
        'vit-L-14': {
            'vision': {
                'hidden_size': 1024,
                'seq_len': 257,
                'layer_num': 24,
            },
            'text': {
                'hidden_size': 768,
                'seq_len': 77,
                'layer_num': 12,
            }
        },
        'vit-H-14': {
            'vision': {
                'hidden_size': 1280,
                'seq_len': 257,
                'layer_num': 32,
            },
            'text': {
                'hidden_size': 1024,
                'seq_len': 77,
                'layer_num': 24,
            }
        },
        'vit-g-14': {
            'vision': {
                'hidden_size': 1408,
                'seq_len': 257,
                'layer_num': 40,
            },
            'text': {
                'hidden_size': 1024,
                'seq_len': 77,
                'layer_num': 24,
            }
        },
        'vit-bigG-14': {
            'vision': {
                'hidden_size': 1664,
                'seq_len': 257,
                'layer_num': 48,
            },
            'text': {
                'hidden_size': 1280,
                'seq_len': 77,
                'layer_num': 32,
            }
        },
    }[model_type]

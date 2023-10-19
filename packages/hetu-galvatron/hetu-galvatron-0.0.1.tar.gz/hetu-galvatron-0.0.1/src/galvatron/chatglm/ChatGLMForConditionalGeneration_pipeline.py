import torch
import torch.nn as nn
from torch.nn.utils import skip_init

class ChatGLMEmbeddings_(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        model = model.transformer
        self.word_embeddings = model.word_embeddings
        self.get_masks = model.get_masks
        self.get_position_ids = model.get_position_ids
        
        # attrs = ['word_embeddings', 'get_masks, 'get_position_ids']
        # for key in attrs:
        #     setattr(self, key, getattr(model, key))
    
    def forward(self, input_ids, position_ids=None, attention_mask=None):
        inputs_embeds = self.word_embeddings(input_ids)

        if attention_mask is None:
            attention_mask = self.get_masks(
                input_ids,
                device=input_ids.device
            )

        if position_ids is None:
            MASK, gMASK = self.config.mask_token_id, self.config.gmask_token_id
            seqs = input_ids.tolist()

            mask_positions, use_gmasks = [], []
            for seq in seqs:
                mask_token = gMASK if gMASK in seq else MASK
                use_gmask = mask_token == gMASK
                mask_positions.append(seq.index(mask_token))
                use_gmasks.append(use_gmask)

            position_ids = self.get_position_ids(
                input_ids,
                mask_positions=mask_positions,
                device=input_ids.device,
                use_gmasks=use_gmasks
            )
        
        # comment this line to remain the shape: [batch, seq_len, hidden_size]
        # hidden_states = inputs_embeds.transpose(0, 1)
        hidden_states = inputs_embeds

        if attention_mask is None:
            attention_mask = torch.zeros(1, 1, device=input_ids.device).bool()
        else:
            attention_mask = attention_mask.to(hidden_states.device)
        
        return hidden_states, position_ids, attention_mask


class ChatGLMlayer_(nn.Module):
    def __init__(self, config, model, layer_idx):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        self.layer = model.transformer.layers[layer_idx]
    
    def forward(self, hidden_states, position_ids, attention_mask):
        layer_ret = self.layer(
            hidden_states=hidden_states,
            position_ids=position_ids,
            attention_mask=attention_mask,
            layer_id=torch.tensor(self.layer_idx)
        )
        hidden_states = layer_ret[0]

        return hidden_states, position_ids, attention_mask


class ChatGLMNorm_(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        self.final_layernorm = model.transformer.final_layernorm
    
    def forward(self, hidden_states, position_ids, attention_mask):
        hidden_states = hidden_states.permute(1, 0, 2)
        hidden_states = self.final_layernorm(hidden_states)
        return hidden_states


class ChatGLMLMHead_(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        self.lm_head = model.lm_head

    def forward(self, hidden_states):
        lm_logits = self.lm_head(hidden_states).permute(1, 0, 2).contiguous()
        return lm_logits

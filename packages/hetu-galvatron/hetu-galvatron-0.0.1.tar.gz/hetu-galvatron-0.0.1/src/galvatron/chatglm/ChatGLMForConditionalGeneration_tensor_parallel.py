import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
from megatron.model.utils import init_method_normal, scaled_init_method_normal
from megatron import get_args
from megatron_layers import ParallelMLP, ParallelAttention
from megatron.model.enums import AttnMaskType, AttnType
from megatron.core import tensor_parallel

try:
    from einops import rearrange
except ImportError:
    rearrange = None

def rotate_half(x):
    x1, x2 = x[..., :x.shape[-1] // 2], x[..., x.shape[-1] // 2:]
    return torch.cat((-x2, x1), dim=x1.ndim - 1)  # dim=-1 triggers a bug in earlier torch versions

@torch.jit.script
def apply_rotary_pos_emb_index(q, k, cos, sin, position_id):
    # position_id: [sq, b], q, k: [sq, b, np, hn], cos: [sq, 1, hn] -> [sq, b, 1, hn]
    cos, sin = F.embedding(position_id, cos.squeeze(1)).unsqueeze(2), \
        F.embedding(position_id, sin.squeeze(1)).unsqueeze(2)
    q, k = (q * cos) + (rotate_half(q) * sin), (k * cos) + (rotate_half(k) * sin)
    return q, k

# implementation in ChatGLM-6B huggingface repo
# def attention_fn(
#         self,
#         query_layer,
#         key_layer,
#         value_layer,
#         attention_mask,
#         hidden_size_per_partition,
#         layer_id,
#         layer_past=None,
#         scaling_attention_score=True,
#         use_cache=False,
# ):
#     if layer_past is not None:
#         past_key, past_value = layer_past[0], layer_past[1]
#         key_layer = torch.cat((past_key, key_layer), dim=0)
#         value_layer = torch.cat((past_value, value_layer), dim=0)

#     # seqlen, batch, num_attention_heads, hidden_size_per_attention_head
#     seq_len, b, nh, hidden_size = key_layer.shape

#     if use_cache:
#         present = (key_layer, value_layer)
#     else:
#         present = None

#     query_key_layer_scaling_coeff = float(layer_id + 1)
#     if scaling_attention_score:
#         query_layer = query_layer / (math.sqrt(hidden_size) * query_key_layer_scaling_coeff)

#     # ===================================
#     # Raw attention scores. [b, np, s, s]
#     # ===================================

#     # [b, np, sq, sk]
#     output_size = (query_layer.size(1), query_layer.size(2), query_layer.size(0), key_layer.size(0))

#     # [sq, b, np, hn] -> [sq, b * np, hn]
#     query_layer = query_layer.view(output_size[2], output_size[0] * output_size[1], -1)
#     # [sk, b, np, hn] -> [sk, b * np, hn]
#     key_layer = key_layer.view(output_size[3], output_size[0] * output_size[1], -1)

#     matmul_result = torch.zeros(
#         1, 1, 1,
#         dtype=query_layer.dtype,
#         device=query_layer.device,
#     )

#     matmul_result = torch.baddbmm(
#         matmul_result,
#         query_layer.transpose(0, 1),  # [b * np, sq, hn]
#         key_layer.transpose(0, 1).transpose(1, 2),  # [b * np, hn, sk]
#         beta=0.0,
#         alpha=1.0,
#     )

#     # change view to [b, np, sq, sk]
#     attention_scores = matmul_result.view(*output_size)

#     if self.scale_mask_softmax:
#         self.scale_mask_softmax.scale = query_key_layer_scaling_coeff
#         attention_probs = self.scale_mask_softmax(attention_scores, attention_mask.contiguous())
#     else:
#         if not (attention_mask == 0).all():
#             # if auto-regressive, skip
#             attention_scores.masked_fill_(attention_mask, -10000.0)
#         dtype = attention_scores.dtype
#         attention_scores = attention_scores.float()
#         attention_scores = attention_scores * query_key_layer_scaling_coeff

#         attention_probs = F.softmax(attention_scores, dim=-1)

#         attention_probs = attention_probs.type(dtype)

#     # =========================
#     # Context layer. [sq, b, hp]
#     # =========================

#     # value_layer -> context layer.
#     # [sk, b, np, hn] --> [b, np, sq, hn]

#     # context layer shape: [b, np, sq, hn]
#     output_size = (value_layer.size(1), value_layer.size(2), query_layer.size(0), value_layer.size(3))

#     # change view [sk, b * np, hn]
#     value_layer = value_layer.view(value_layer.size(0), output_size[0] * output_size[1], -1)

#     # change view [b * np, sq, sk]
#     attention_probs = attention_probs.view(output_size[0] * output_size[1], output_size[2], -1)

#     # matmul: [b * np, sq, hn]
#     context_layer = torch.bmm(attention_probs, value_layer.transpose(0, 1))

#     # change view [b, np, sq, hn]
#     context_layer = context_layer.view(*output_size)

#     # [b, np, sq, hn] --> [sq, b, np, hn]
#     context_layer = context_layer.permute(2, 0, 1, 3).contiguous()

#     # [sq, b, np, hn] --> [sq, b, hp]
#     new_context_layer_shape = context_layer.size()[:-2] + (hidden_size_per_partition,)
#     context_layer = context_layer.view(*new_context_layer_shape)

#     outputs = (context_layer, present, attention_probs)

#     return outputs

class ChatGLMSelfAttention_tp(nn.Module):
    def __init__(self, config, glm_block, tp_group=None):
        super().__init__()
        args=get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        self.config = config
        self.position_encoding_2d = glm_block.attention.position_encoding_2d
        self.rotary_emb = glm_block.attention.rotary_emb

        self.attention = ParallelAttention(init_method,
                                        scaled_init_method,
                                        attention_type=AttnType.self_attn,
                                        attn_mask_type=AttnMaskType.causal, # GLM attn mask is non-causal + causal
                                        tp_group=self.tp_group)
    
    def forward(self, hidden_states, position_ids, attention_mask, layer_id, layer_past=None, use_cache=False, output_attentions=False):
        """
        hidden_states: [seq_len, batch, hidden_size]
        attention_mask: [(1, 1), seq_len, seq_len]
        """

        # [seq_len, batch, 3 * hidden_size]
        mixed_raw_layer, _ = self.attention.query_key_value(hidden_states) # zsh comment: Megatron impl has no bias but ChatGLM impl has

        # [seq_len, batch, 3 * hidden_size] --> [seq_len, batch, num_attention_heads, 3 * hidden_size_per_attention_head]
        new_tensor_shape = mixed_raw_layer.size()[:-1] + (
            self.attention.num_attention_heads_per_partition,
            3 * self.attention.hidden_size_per_attention_head,
        )
        mixed_raw_layer = mixed_raw_layer.view(*new_tensor_shape)

        # [seq_len, batch, num_attention_heads, hidden_size_per_attention_head]
        (query_layer, key_layer, value_layer) = tensor_parallel.split_tensor_along_last_dim(mixed_raw_layer, 3)

        if self.position_encoding_2d:
            q1, q2 = query_layer.chunk(2, dim=(query_layer.ndim - 1))
            k1, k2 = key_layer.chunk(2, dim=(key_layer.ndim - 1))
            cos, sin = self.rotary_emb(q1, seq_len=position_ids.max() + 1)
            position_ids, block_position_ids = position_ids[:, 0, :].transpose(0, 1).contiguous(), \
                position_ids[:, 1, :].transpose(0, 1).contiguous()
            q1, k1 = apply_rotary_pos_emb_index(q1, k1, cos, sin, position_ids)
            q2, k2 = apply_rotary_pos_emb_index(q2, k2, cos, sin, block_position_ids)
            query_layer = torch.concat([q1, q2], dim=(q1.ndim - 1))
            key_layer = torch.concat([k1, k2], dim=(k1.ndim - 1))
        else:
            position_ids = position_ids.transpose(0, 1)
            cos, sin = self.rotary_emb(value_layer, seq_len=position_ids.max() + 1)
            # [seq_len, batch, num_attention_heads, hidden_size_per_attention_head]
            query_layer, key_layer = apply_rotary_pos_emb_index(query_layer, key_layer, cos, sin, position_ids)

        # [seq_len, batch, hidden_size]
        
        # implementation in ChatGLM-6B huggingface repo
        # context_layer = attention_fn(
        #     self=self,
        #     query_layer=query_layer,
        #     key_layer=key_layer,
        #     value_layer=value_layer,
        #     attention_mask=attention_mask,
        #     hidden_size_per_partition=self.hidden_size_per_partition,
        #     layer_id=layer_id
        # )

        # implementation in megatron
        if not self.attention.use_flash_attn:
            if self.attention.checkpoint_core_attention:
                context_layer = self.attention._checkpointed_attention_forward(
                    query_layer, key_layer, value_layer, attention_mask)
            else:
                context_layer = self.attention.core_attention(
                    query_layer, key_layer, value_layer, attention_mask)
        else:
            q, k, v = [rearrange(x, 's b ... -> b s ...').contiguous()
                       for x in (query_layer, key_layer, value_layer)]
            if not self.attention.sequence_parallel:
                with tensor_parallel.get_cuda_rng_tracker().fork():
                    context_layer = self.attention.core_attention_flash(q, k, v)
            else:
                context_layer = self.attention.core_attention_flash(q, k, v)
            context_layer = rearrange(context_layer, 'b s h d -> s b (h d)').contiguous()
        

        output, bias = self.attention.dense(context_layer)
        output = output + bias # zsh add to fit ChatGLM

        outputs = (output, None, None)

        return outputs  # output, present, attention_probs


class ChatGLMGLU_tp(nn.Module):
    def __init__(self, config, tp_group=None):
        super().__init__()
        args = get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        # should set args.openai_gelu = True
        args.openai_gelu = True
        self.mlp = ParallelMLP(init_method, scaled_init_method, tp_group=self.tp_group)

    def forward(self, hidden_states):
        hidden_states, bias = self.mlp(hidden_states)
        return hidden_states + bias


class GLMBlock_tp(nn.Module):
    def __init__(self, config, glm_block):
        super().__init__()
        self.config = config
        self.glm_block = glm_block
    
    def forward(self, hidden_states, position_ids, attention_mask, layer_id):
        hidden_states = hidden_states.permute(1, 0, 2)
        outputs = self.glm_block(hidden_states, position_ids, attention_mask, layer_id)
        outputs = (outputs[0].permute(1, 0, 2),)
        return outputs
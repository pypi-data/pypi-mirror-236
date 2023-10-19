import torch
from torch import nn
from torch import Tensor, device
from typing import Tuple
import sys
from megatron.model.utils import init_method_normal, scaled_init_method_normal
from megatron import get_args
from megatron_layers import ParallelMLP, ParallelAttention
from megatron.model.enums import AttnMaskType, AttnType

class GPTMLP_tp(nn.Module):
    def __init__(self, config, tp_group = None):
        super().__init__()
        args=get_args()
        args.bias_gelu_fusion = True
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        self.mlp = ParallelMLP(init_method, scaled_init_method, tp_group = self.tp_group)

    def forward(self, hidden_states):
        hidden_states, _ = self.mlp(hidden_states)
        return hidden_states
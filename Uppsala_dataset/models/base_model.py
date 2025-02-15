import torch
import torch.nn as nn

class BaseModel(nn.Module):
    def __init__(self):
        super().__init__()
        
    def get_trainable_params(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
        
    def get_parameter_count(self):
        return {name: p.numel() for name, p in self.named_parameters()}
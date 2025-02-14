import torch
import torch.nn as nn
from .base_model import BaseModel

class MLPModel(BaseModel):
    def __init__(self, input_dim, output_dim, hidden_layers=[256, 256, 256], 
                 dropout_rate=0.2, l2_penalty=1e-5):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        # Build hidden layers
        for hidden_dim in hidden_layers:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout_rate),
                nn.BatchNorm1d(hidden_dim)
            ])
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.model = nn.Sequential(*layers)
        self.l2_penalty = l2_penalty
        
    def forward(self, x):
        return self.model(x)
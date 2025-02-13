import torch
import torch.nn as nn
from .base_model import BaseModel
import numpy as np

class CNNModel(BaseModel):
    def __init__(self, input_dim, output_dim, num_channels=[32, 64, 128], 
                 kernel_sizes=[3, 3, 3], dropout_rate=0.3):
        super().__init__()
        
        if input_dim <= 0:
            raise ValueError(f"Input dimension must be positive, got {input_dim}")
            
        self.input_reshape = input_dim
        self.num_channels = num_channels
        
        # Determine number of pooling layers based on input dimension
        max_pools = int(np.log2(input_dim)) - 1  # Keep at least 2 features
        num_channels = num_channels[:max_pools]
        kernel_sizes = kernel_sizes[:max_pools]
        
        # CNN layers
        cnn_layers = []
        in_channels = 1
        current_dim = input_dim
        
        for out_channels, kernel_size in zip(num_channels, kernel_sizes):
            kernel_size = min(kernel_size, current_dim)
            
            cnn_layers.extend([
                nn.Conv1d(in_channels, out_channels, kernel_size, padding='same'),
                nn.ReLU(),
                nn.MaxPool1d(2),
                nn.BatchNorm1d(out_channels),
                nn.Dropout(dropout_rate)
            ])
            in_channels = out_channels
            current_dim = current_dim // 2  # Update dimension after pooling
            
        self.cnn_layers = nn.Sequential(*cnn_layers)
        
        # Calculate the size of flattened output
        self.flatten_size = current_dim * num_channels[-1]
        
        if self.flatten_size <= 0:
            raise ValueError(f"Calculated flatten size must be positive, got {self.flatten_size}")
        
        # Fully connected layers with adjusted input size
        self.fc_layers = nn.Sequential(
            nn.Linear(self.flatten_size, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, output_dim)
        )
        
    def forward(self, x):
        # Add assertion to check input dimensions
        assert x.size(0) > 0, "Batch size must be positive"
        assert x.size(1) == self.input_reshape, f"Expected input dimension {self.input_reshape}, got {x.size(1)}"
        
        # Reshape input: (batch_size, features) -> (batch_size, 1, features)
        x = x.unsqueeze(1)
        x = self.cnn_layers(x)
        # Flatten: (batch_size, channels, features) -> (batch_size, channels * features)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x
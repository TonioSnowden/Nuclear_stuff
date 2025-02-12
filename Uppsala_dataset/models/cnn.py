import torch
import torch.nn as nn
from .base_model import BaseModel

class CNNModel(BaseModel):
    def __init__(self, input_dim, output_dim, num_channels=[32, 64, 128], 
                 kernel_sizes=[3, 3, 3], dropout_rate=0.3):
        super().__init__()
        
        self.input_reshape = input_dim
        
        # CNN layers
        cnn_layers = []
        in_channels = 1  # Start with 1 channel for 1D input
        
        for out_channels, kernel_size in zip(num_channels, kernel_sizes):
            cnn_layers.extend([
                nn.Conv1d(in_channels, out_channels, kernel_size, padding='same'),
                nn.ReLU(),
                nn.MaxPool1d(2),
                nn.BatchNorm1d(out_channels),
                nn.Dropout(dropout_rate)
            ])
            in_channels = out_channels
            
        self.cnn_layers = nn.Sequential(*cnn_layers)
        
        # Calculate the size of flattened output
        self.flatten_size = self._get_flatten_size(input_dim, len(num_channels))
        
        # Fully connected layers
        self.fc_layers = nn.Sequential(
            nn.Linear(self.flatten_size, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, output_dim)
        )
        
    def _get_flatten_size(self, input_dim, num_pools):
        # Calculate size after pooling operations
        return (input_dim // (2 ** num_pools)) * self.num_channels[-1]
        
    def forward(self, x):
        # Reshape input: (batch_size, features) -> (batch_size, 1, features)
        x = x.unsqueeze(1)
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.fc_layers(x)
        return x
import torch
import torch.nn as nn
from .base_model import BaseModel

class OptimizedNuclearNet(BaseModel):
    def __init__(self, input_dim, output_dim, hidden_dims=[512, 256, 128, 64]):
        super().__init__()
        
        # First branch: Dense feature extraction
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_dim, hidden_dims[0]),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dims[0]),
            nn.Dropout(0.3),
            
            nn.Linear(hidden_dims[0], hidden_dims[1]),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dims[1]),
            nn.Dropout(0.3)
        )
        
        # Second branch: Residual connection
        self.residual = nn.Sequential(
            nn.Linear(input_dim, hidden_dims[1]),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dims[1])
        )
        
        # Combine and process
        self.combined_processor = nn.Sequential(
            nn.Linear(hidden_dims[1] * 2, hidden_dims[2]),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dims[2]),
            nn.Dropout(0.2),
            
            nn.Linear(hidden_dims[2], hidden_dims[3]),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(hidden_dims[3]),
            nn.Dropout(0.1)
        )
        
        # Output layer with isotope-specific considerations
        self.output_layer = nn.Sequential(
            nn.Linear(hidden_dims[3], output_dim),
            nn.Softplus()  # Ensures positive outputs for isotope concentrations
        )
        
    def forward(self, x):
        # Feature extraction path
        features = self.feature_extractor(x)
        
        # Residual path
        residual = self.residual(x)
        
        # Combine paths
        combined = torch.cat([features, residual], dim=1)
        
        # Process combined features
        processed = self.combined_processor(combined)
        
        # Generate output
        return self.output_layer(processed) 
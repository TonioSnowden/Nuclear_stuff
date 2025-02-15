import torch
import torch.nn as nn
from .base_model import BaseModel
from .mlp import MLPModel

class PINNModel(BaseModel):
    def __init__(self, input_dim, output_dim, hidden_layers=[256, 256, 256], 
                 dropout_rate=0.3):
        super().__init__()
        
        self.mlp = MLPModel(input_dim, output_dim, hidden_layers, dropout_rate)
        
    def forward(self, x):
        predictions = self.mlp(x)
        return predictions
    
    def physics_loss(self, predictions, decay_constants):
        """
        Implement physics-based constraints for U and Pu isotopes
        """
        # Get indices for relevant isotopes
        u238_idx = 0  # fuel_U238
        u235_idx = 1  # fuel_U235
        pu239_idx = 2  # fuel_Pu239
        u236_idx = 3  # fuel_U236
        u234_idx = 4  # fuel_U234
        
        # Extract predictions for each isotope
        u238 = predictions[:, u238_idx]
        u235 = predictions[:, u235_idx]
        pu239 = predictions[:, pu239_idx]
        u236 = predictions[:, u236_idx]
        u234 = predictions[:, u234_idx]
        
        # Physics constraints:
        
        # 1. Mass conservation (sum of mass fractions should be close to 1)
        mass_conservation = torch.abs(u238 + u235 + pu239 + u236 + u234 - 1.0)
        
        # 2. U238 should be the most abundant isotope
        abundance_constraint = torch.relu(u235 - u238) + torch.relu(pu239 - u238) + \
                             torch.relu(u236 - u238) + torch.relu(u234 - u238)
        
        # 3. Natural decay chain relationships
        # U238 -> U234 decay relationship
        u238_u234_decay = torch.abs(u234 - decay_constants.get('U238_U234', 1e-6) * u238)
        
        # U235 -> Pu239 relationship through neutron capture
        u235_pu239_relation = torch.abs(pu239 - decay_constants.get('U235_Pu239', 1e-4) * u235)
        
        # Combine all physics losses
        total_physics_loss = (
            0.4 * torch.mean(mass_conservation) +
            0.3 * torch.mean(abundance_constraint) +
            0.2 * torch.mean(u238_u234_decay) +
            0.1 * torch.mean(u235_pu239_relation)
        )
        
        return total_physics_loss
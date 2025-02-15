import torch
import torch.nn as nn

class RelativeDensityLoss(nn.Module):
    def __init__(self, epsilon=1e-7):
        super().__init__()
        self.epsilon = epsilon  
        
    def forward(self, predictions, targets):
        relative_diff = torch.abs(predictions - targets) / (targets + self.epsilon)
        weights = torch.log1p(torch.abs(targets))
        weighted_loss = relative_diff * weights
        
        return torch.mean(weighted_loss) 
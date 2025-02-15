import torch
import torch.nn as nn

class PercentageRMSELoss(nn.Module):
    def __init__(self, epsilon=1e-7):
        super().__init__()
        self.epsilon = epsilon
        
    def forward(self, predictions, targets):
        # Calculate percentage difference
        percentage_diff = (predictions - targets) / (torch.abs(targets) + self.epsilon)
        
        # Square the percentage differences (emphasizes large deviations)
        squared_perc_diff = torch.pow(percentage_diff, 2)
        
        # Calculate RMSE
        rmse = torch.sqrt(torch.mean(squared_perc_diff) + self.epsilon)
        
        return rmse 
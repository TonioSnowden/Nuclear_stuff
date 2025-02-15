import torch
import torch.nn as nn

class PercentageRMSELoss(nn.Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, predictions, targets):
        # Calculate percentage difference
        percentage_diff = 100* ((predictions - targets) / (torch.abs(targets)))
        
        # Square the percentage differences (emphasizes large deviations)
        squared_perc_diff = torch.pow(percentage_diff, 2)
        
        # Calculate RMSE
        rmse = torch.sqrt(torch.mean(squared_perc_diff))
        
        return rmse 
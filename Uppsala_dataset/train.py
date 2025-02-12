import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import numpy as np
from models import MLPModel, CNNModel, PINNModel
import wandb  # For experiment tracking

class NuclearModelTrainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def prepare_data(self, X, y):
        # Convert to PyTorch tensors
        X_tensor = torch.FloatTensor(X.values)
        y_tensor = torch.FloatTensor(y.values)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X_tensor, y_tensor, test_size=0.2, random_state=42
        )
        
        # Create data loaders
        train_dataset = TensorDataset(X_train, y_train)
        val_dataset = TensorDataset(X_val, y_val)
        
        self.train_loader = DataLoader(
            train_dataset, 
            batch_size=self.config['batch_size'], 
            shuffle=True
        )
        self.val_loader = DataLoader(
            val_dataset, 
            batch_size=self.config['batch_size']
        )
        
        return X_train.shape[1], y_train.shape[1]
    
    def train_model(self, X, y):
        input_dim, output_dim = self.prepare_data(X, y)
        
        # Initialize model based on config
        if self.config['model_type'] == 'mlp':
            model = MLPModel(
                input_dim=input_dim,
                output_dim=output_dim,
                hidden_layers=self.config['hidden_layers'],
                dropout_rate=self.config['dropout_rate']
            )
        elif self.config['model_type'] == 'cnn':
            model = CNNModel(
                input_dim=input_dim,
                output_dim=output_dim,
                num_channels=self.config['num_channels'],
                kernel_sizes=self.config['kernel_sizes']
            )
        elif self.config['model_type'] == 'pinn':
            model = PINNModel(
                input_dim=input_dim,
                output_dim=output_dim,
                hidden_layers=self.config['hidden_layers']
            )
            
        model = model.to(self.device)
        
        # Initialize optimizer
        optimizer = torch.optim.Adam(
            model.parameters(), 
            lr=self.config['learning_rate'],
            weight_decay=self.config.get('l2_penalty', 0)
        )
        
        # Initialize loss function
        criterion = nn.MSELoss()
        
        # Training loop
        for epoch in range(self.config['epochs']):
            model.train()
            train_loss = 0
            
            for batch_X, batch_y in self.train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                
                if self.config['model_type'] == 'pinn':
                    physics_loss = model.physics_loss(outputs, self.config['decay_constants'])
                    loss += self.config['physics_weight'] * physics_loss
                
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch_X, batch_y in self.val_loader:
                    batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                    outputs = model(batch_X)
                    val_loss += criterion(outputs, batch_y).item()
            
            # Log metrics
            wandb.log({
                'epoch': epoch,
                'train_loss': train_loss / len(self.train_loader),
                'val_loss': val_loss / len(self.val_loader)
            })
            
        return model 
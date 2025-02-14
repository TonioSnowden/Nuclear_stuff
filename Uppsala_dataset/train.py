import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import numpy as np
from models.mlp import MLPModel
from models.cnn import CNNModel, DensityLoss
from models.pinn import PINNModel

class NuclearModelTrainer:
    def __init__(self, config, model_dir):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_dir = model_dir
        
        # Initialize loss function
        if config.get('loss_function') == 'density':
            self.criterion = DensityLoss()
        else:
            self.criterion = nn.MSELoss()
        
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
                dropout_rate=self.config['dropout_rate'],
                l2_penalty=self.config['l2_penalty']
            )
        elif self.config['model_type'] == 'cnn':
            model = CNNModel(
                input_dim=input_dim,
                output_dim=output_dim,
                num_channels=self.config['num_channels'],
                kernel_sizes=self.config['kernel_sizes'],
                dropout_rate=self.config['dropout_rate']
            )
        elif self.config['model_type'] == 'pinn':
            model = PINNModel(
                input_dim=input_dim,
                output_dim=output_dim,
                hidden_layers=self.config['hidden_layers'],
                dropout_rate=self.config['dropout_rate']
            )
            
        model = model.to(self.device)
        
        # Initialize optimizer
        optimizer = torch.optim.Adam(
            model.parameters(), 
            lr=self.config['learning_rate'],
            weight_decay=self.config.get('l2_penalty', 0)
        )
        
        history = {
            'train_loss': [],
            'val_loss': []
        }
        
        # Initialize learning rate scheduler
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=0.5,
            patience=5,
            verbose=True
        )

        for epoch in range(self.config['epochs']):
            model.train()
            train_loss = 0
            
            for batch_X, batch_y in self.train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(batch_X)
                
                # Check for NaN values
                if torch.isnan(outputs).any():
                    print(f"NaN detected in outputs at epoch {epoch}")
                    continue
                
                loss = self.criterion(outputs, batch_y)
                
                if torch.isnan(loss):
                    print(f"NaN detected in loss at epoch {epoch}")
                    continue
                
                if self.config['model_type'] == 'pinn':
                    physics_loss = model.physics_loss(outputs, self.config['decay_constants'])
                    if not torch.isnan(physics_loss):
                        loss += self.config['physics_weight'] * physics_loss
                
                loss.backward()
                
                # Gradient clipping to prevent exploding gradients
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
                
                optimizer.step()
                
                train_loss += loss.item()
            
            # Calculate average training loss
            avg_train_loss = train_loss / len(self.train_loader)
            
            # Validation
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch_X, batch_y in self.val_loader:
                    batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                    outputs = model(batch_X)
                    val_loss += self.criterion(outputs, batch_y).item()
            
            # Calculate average validation loss
            avg_val_loss = val_loss / len(self.val_loader)
            
            # Store in history
            history['train_loss'].append(float(avg_train_loss))
            history['val_loss'].append(float(avg_val_loss))
            
            # Print progress every epoch for the small dataset
            print(f'Epoch [{epoch+1}/{self.config["epochs"]}], '
                  f'Train Loss: {avg_train_loss:.6f}, '
                  f'Val Loss: {avg_val_loss:.6f}')
        
            scheduler.step(avg_val_loss)
        
        return model, history 
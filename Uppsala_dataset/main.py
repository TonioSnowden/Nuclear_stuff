import torch
import os
import json
from datetime import datetime
from train import NuclearModelTrainer
import pandas as pd
import numpy as np

# Configuration for different models
configs = {
    'mlp': {
        'model_type': 'mlp',
        'hidden_layers': [512, 256, 128],
        'dropout_rate': 0.2,
        'l2_penalty': 1e-6,
        'batch_size': 32,
        'learning_rate': 0.0005,
        'epochs': 200,
        'loss_function': 'percentage_rmse'
    },
    'cnn': {
        'model_type': 'cnn',
        'num_channels': [32, 64, 128],
        'kernel_sizes': [3, 3, 3],
        'dropout_rate': 0.3,
        'batch_size': 64,
        'learning_rate': 0.001,
        'epochs': 100,
        'loss_function': 'percentage_rmse'
    },
    'pinn': {
        'model_type': 'pinn',
        'hidden_layers': [512, 256, 128],
        'dropout_rate': 0.3,
        'physics_weight': 0.1,
        'decay_constants': {
            'U238_U234': 1e-6,  # Approximate decay constant
            'U235_Pu239': 1e-4,  # Approximate neutron capture rate
        },
        'batch_size': 64,
        'learning_rate': 0.001,
        'epochs': 100,
        'loss_function': 'percentage_rmse'
    },
    'nuclear_net': {
        'model_type': 'nuclear_net',
        'hidden_dims': [512, 256, 128, 64],
        'dropout_rate': 0.3,
        'batch_size': 64,
        'learning_rate': 0.001,
        'epochs': 200,
        'loss_function': 'percentage_rmse'
    }
}

def setup_logging(model_type):
    # Create directories if they don't exist
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir = f'runs/{model_type}_{timestamp}'
    model_dir = f'{log_dir}/models'
    os.makedirs(model_dir, exist_ok=True)
    
    return log_dir, model_dir

def load_data():
    # Load your data here
    df = pd.read_csv('top10_nuclear.csv')
    
    # Define your features and targets
    input_features = ["AN", "SF", "fuel_TOT_GS", "fuel_TOT_DH",	"fuel_TOT_A"]
    output_features = [
    'fuel_U238', 'fuel_U235', 'fuel_Pu239', 'fuel_U236', 'fuel_U234'
    ]

    print("Features size")
    print(len(input_features))
    print(len(output_features))
    
    X = df[input_features]
    y = df[output_features]
    
    # Normalize the data
    X = (X - X.mean()) / X.std()
    y = (y - y.mean()) / y.std()
    
    # Check for any infinite or NaN values
    if X.isnull().any().any() or y.isnull().any().any():
        raise ValueError("Dataset contains NaN values")
    if np.isinf(X.values).any() or np.isinf(y.values).any():
        raise ValueError("Dataset contains infinite values")
    
    return X, y

def main():
    # Choose model type
    model_type = 'nuclear_net'
    config = configs[model_type]
    
    # Setup logging directories
    log_dir, model_dir = setup_logging(model_type)
    
    # Save configuration
    with open(f'{log_dir}/config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    # Load data
    X, y = load_data()
    
    # Initialize trainer with custom loss
    trainer = NuclearModelTrainer(config, model_dir)
    
    # Train model and get training history
    model, history = trainer.train_model(X, y)
    
    # Save training history
    with open(f'{log_dir}/training_history.json', 'w') as f:
        json.dump(history, f, indent=4)
    
    # Save model
    torch.save({
        'model_state_dict': model.state_dict(),
        'config': config,
        'history': history
    }, f'{model_dir}/{model_type}_model.pt')
    
    print(f"Training completed. Logs and model saved in {log_dir}")

if __name__ == "__main__":
    main()
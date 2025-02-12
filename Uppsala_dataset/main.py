import wandb
from train import NuclearModelTrainer

# Configuration for different models
configs = {
    'mlp': {
        'model_type': 'mlp',
        'hidden_layers': [512, 256, 128],
        'dropout_rate': 0.3,
        'l2_penalty': 1e-5,
        'batch_size': 64,
        'learning_rate': 0.001,
        'epochs': 100
    },
    'cnn': {
        'model_type': 'cnn',
        'num_channels': [32, 64, 128],
        'kernel_sizes': [3, 3, 3],
        'dropout_rate': 0.3,
        'batch_size': 64,
        'learning_rate': 0.001,
        'epochs': 100
    },
    'pinn': {
        'model_type': 'pinn',
        'hidden_layers': [512, 256, 128],
        'dropout_rate': 0.3,
        'physics_weight': 0.1,
        'decay_constants': {
            'Pu241_Am241': 0.0483  # Example decay constant
        },
        'batch_size': 64,
        'learning_rate': 0.001,
        'epochs': 100
    }
}

def main():
    # Initialize wandb
    wandb.init(project="nuclear-ml")
    
    # Choose model type
    model_type = 'mlp'  # or 'cnn' or 'pinn'
    config = configs[model_type]
    
    # Initialize trainer
    trainer = NuclearModelTrainer(config)
    
    # Train model
    model = trainer.train_model(X, y)  # Replace X, y with your data
    
    # Save model
    torch.save(model.state_dict(), f'models/{model_type}_model.pt')

if __name__ == "__main__":
    main() 
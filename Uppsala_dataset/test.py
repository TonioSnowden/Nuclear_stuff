import torch
import json
import pandas as pd
import numpy as np
from models.cnn import CNNModel

def load_model_and_config(model_path, config_path):
    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Load data to get input/output dimensions
    df = pd.read_csv('top10_nuclear.csv')
    input_features = ["AN", "SF", "fuel_TOT_GS", "fuel_TOT_DH", "fuel_TOT_A"]
    #output_features = [col for col in df.columns if col.startswith('fuel_')]
    #output_features = [col for col in output_features if col not in input_features]
    output_features = [
    'fuel_U238', 'fuel_U235', 'fuel_Pu239', 'fuel_U236', 'fuel_U234'
    ]

    
    # Initialize model with same configuration
    model = CNNModel(
        input_dim=len(input_features),
        output_dim=len(output_features),
        num_channels=config['num_channels'],
        kernel_sizes=config['kernel_sizes'],
        dropout_rate=config['dropout_rate']
    )
    
    # Load trained weights
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()  # Set to evaluation mode
    
    return model, config, input_features, output_features

def predict(model, input_data, input_features):
    # Normalize input data (using same method as in training)
    input_data = (input_data - input_data.mean()) / input_data.std()
    
    # Convert to tensor
    input_tensor = torch.FloatTensor(input_data.values)
    
    # Make prediction
    with torch.no_grad():
        prediction = model(input_tensor)
    
    return prediction.numpy()

def main():
    # Load model and configuration
    model, config, input_features, output_features = load_model_and_config(
        'runs/cnn_20250215_041256/models/cnn_model.pt',  # Replace with your model path
        'runs/cnn_20250215_041256/config.json'  # Replace with your config path
    )
    
    # Load some test data
    df = pd.read_csv('top10_nuclear.csv', nrows=1000)
    test_data = df[input_features].head(5)  # Get first 5 samples as example
    test_output = df[output_features].head(5)
    
    # Make predictions
    predictions = predict(model, test_data, input_features)
    
    # Print results
    print("\nPredictions for first 5 samples:")
    for i, pred in enumerate(predictions):
        print("True response")
        print(test_output.iloc[i])        
        print(f"\nSample {i+1}:")
        for feat, val in zip(output_features, pred):
            print(f"{feat}: {val:.6f}")

if __name__ == "__main__":
    main()
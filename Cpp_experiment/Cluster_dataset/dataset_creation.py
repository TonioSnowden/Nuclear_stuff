import pandas as pd
import numpy as np
import glob
import argparse

def create_dataset(input_dir, output_file):
    results = []

    for filename in glob.glob(f"{input_dir}/*.txt"):  # Adjust the pattern as needed
        with open(filename, 'r') as f:
            data = f.readlines()
            # Extract relevant data from the output
            density = ...  # Extract density from filename or data
            radius = ...   # Extract radius from filename or data
            particles = ...  # Extract particles from filename or data
            particle_times = ...  # Extract particle times from the output
            gate_widths = ...  # Extract gate widths from the output
            y_values = ...  # Extract y values from the output

            results.append({
                'density': density,
                'radius': radius,
                'particles': particles,
                'particle_times': particle_times,
                'gate_widths': gate_widths,
                'y_values': y_values
            })

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Dataset created successfully and saved to {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create dataset from simulation results.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing input files.')
    parser.add_argument('--output_file', type=str, required=True, help='Output CSV file name.')
    args = parser.parse_args()

    create_dataset(args.input_dir, args.output_file)
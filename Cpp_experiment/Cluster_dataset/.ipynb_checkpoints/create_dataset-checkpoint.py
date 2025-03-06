import pandas as pd
import numpy as np
import glob

# Initialize lists to store results
results = []

# Assuming the output files are named in a specific way
for filename in glob.glob("output/*.txt"):  # Adjust the pattern as needed
    with open(filename, 'r') as f:
        data = f.readlines()
        # Extract relevant data from the output
        # This is a placeholder; adjust according to your output format
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
df.to_csv('simulation_results.csv', index=False)
print("Dataset created successfully.")
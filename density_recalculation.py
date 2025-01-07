import pandas as pd
import openmc.data
import ast

# Read the CSV file
df = pd.read_csv('df_converted_fuel.csv')
df["fuel_value"] = df["fuel_value"].apply(ast.literal_eval)

def apply_half_life_calculation(fuel_dict):
    """
    Apply half-life calculation to each nuclide in the fuel dictionary.
    Only keeps isotopes that have a half-life.
    """
    modified_densities = {}
    for nuclide, density in fuel_dict.items():
        half_life = openmc.data.half_life(nuclide)  # Get half-life in seconds
        if half_life is not None:  # Only process nuclides with half-life
            atomic_mass = openmc.data.atomic_mass(nuclide)
            modified_densities[nuclide] = density * half_life / atomic_mass
    return modified_densities

# Apply the calculation to each row and create new column
df['fuel_density_half_life'] = df['fuel_value'].apply(apply_half_life_calculation)

# Save the updated dataframe to CSV
df.to_csv('df_converted_fuel_with_half_life_2.csv', index=False)

# Print the first few rows of the new column to verify
print("\nFirst few rows of the new column:")
print(df['fuel_density_half_life'].head())

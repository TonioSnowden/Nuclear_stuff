import openmc
import matplotlib.pyplot as plt
import numpy as np

# Function to plot distribution
def plot_distribution(dist, name, num_samples=10000):
    print(name)
    samples = dist.sample(num_samples)
    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=50, density=True, alpha=0.7)
    plt.title(f'{name} Distribution')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.savefig(f'{name.lower()}_distribution.png')
    plt.close()

# Watt distribution Pu239
watt = openmc.stats.Watt(a=0.885247, b=3.802690)
plot_distribution(watt, 'Watt Pu239')

# Watt distribution Pu240
watt = openmc.stats.Watt(a=0.794930, b=4.689270)
plot_distribution(watt, 'Watt Pu240')

print("All distribution plots have been saved.")
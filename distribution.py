import openmc
import matplotlib.pyplot as plt
import numpy as np

# Function to plot distribution
def plot_distribution(dist, name, num_samples=10000):
    print(name
    samples = dist.sample(num_samples)
    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=50, density=True, alpha=0.7)
    plt.title(f'{name} Distribution')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.savefig(f'{name.lower()}_distribution.png')
    plt.close()

# Discrete distribution
discrete = openmc.stats.Discrete([0, 1, 2], [0.3, 0.5, 0.2])
plot_distribution(discrete, 'Discrete')

# Power

# Uniform distribution
uniform = openmc.stats.Uniform(0, 10)
plot_distribution(uniform, 'Uniform')

# Maxwell distribution
maxwell = openmc.stats.Maxwell(2.0)
plot_distribution(maxwell, 'Maxwell')

# Watt distribution
watt = openmc.stats.Watt(a=0.885247, b=3.802690)
plot_distribution(watt, 'Watt')

# Normal distribution
normal = openmc.stats.Normal(5, 1)
plot_distribution(normal, 'Normal')

# Muir distribution
muir = openmc.stats.Muir(e0=14.08e6, m_rat=0.5, kt=20000.0)
plot_distribution(muir, 'Muir')

# Tabular distribution
x = np.linspace(0, 10, 50)
y = np.exp(-x/3)
tabular = openmc.stats.Tabular(x, y)
plot_distribution(tabular, 'Tabular')

# Legendre distribution
legendre = openmc.stats.Legendre([0.5, 1.0, -0.5])
plot_distribution(legendre, 'Legendre')

# Mixture distribution
mix1 = openmc.stats.Uniform(0, 5)
mix2 = openmc.stats.Normal(7, 1)
mixture = openmc.stats.Mixture([mix1, mix2], [0.3, 0.7])
plot_distribution(mixture, 'Mixture')

print("All distribution plots have been saved.")
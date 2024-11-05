import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Create Cf-252 material
cf252 = openmc.Material(name='Cf-252')
cf252.add_nuclide('Cf252', 1.0)
cf252.set_density('g/cm3', 10.0) 

materials = openmc.Materials([cf252])

# Create geometry - small sphere for source
sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
cell = openmc.Cell(fill=cf252, region=-sphere)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)

def gaussian_energy_distribution(x):
    y0 = 16.48223
    xc = 2.39486
    w = 2.97584
    A = 154.42528
    return y0 + (A / (w * np.sqrt(np.pi / 2))) * np.exp(-2 * ((x - xc) ** 2) / (w ** 2))

# Create x values (energy range)
x = np.linspace(0.5, 8.5, 1000)  # From 0.5 to 8.5 MeV with 1000 points

# Calculate probabilities
probabilities = gaussian_energy_distribution(x)
probabilities /= np.sum(probabilities)  # Normalize probabilities

# Create the source
source = openmc.IndependentSource()

total_time = 10000  # seconds
expected_decays = 28.113 * total_time
print("Expected decay", expected_decays)
source.time = openmc.stats.Uniform(0, total_time)
# Source with time distribution
source.angle = openmc.stats.Isotropic()
source.space = openmc.stats.Point((0, 0, 0))
source.energy = openmc.stats.Tabular(x, probabilities, interpolation='linear-linear')
source.particle = "neutron"


# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = int(expected_decays)
settings.source = source

# Create tallies with 100000 time bins
time_bins = np.linspace(0, 10000, 100000)  
time_filter = openmc.TimeFilter(time_bins)

tally = openmc.Tally()
tally.scores = ['nu-fission']
tally.filters = [openmc.CellFilter(cell), time_filter]

tallies = openmc.Tallies([tally])

# Create and run model
model = openmc.model.Model(geometry, materials, settings, tallies)
sp_filename = model.run()

def process_feynman_histogram(time_events, pre_delay = 0.5, gate_width=10):
    counts_per_gate = []
    
    for i in range(len(time_events['time'])):
        gate_start = time_events['time'].iloc[i] + pre_delay
        gate_end = gate_start + gate_width 
        mask = (time_events['time'] >= gate_start) & (time_events['time'] < gate_end)
        counts = np.sum(time_events['mean'][mask])
        counts_per_gate.append(counts)
        gate_start = gate_end
        
    return np.array(counts_per_gate)

# Process results and create graphs
with openmc.StatePoint(sp_filename) as sp:
    tally_result = sp.get_tally()
    df = tally_result.get_pandas_dataframe()

    print(df)
    print(df['mean'].sum())

    # Extract time and mean values
    time_values = df['time low [s]'] + 0.5 * (df['time high [s]'] - df['time low [s]'])
    mean_values = df['mean'] * 100000

    event_times = pd.DataFrame({
    'time': time_values,
    'mean': mean_values
    })


    print("events created")
    
    # Process using Feynman histogram
    counts = process_feynman_histogram(event_times)
    counts = counts[counts > 50]
    
    print(counts)

    print("feynman count")
    
    # Calculate Feynman statistics
    mean_counts = np.mean(counts)
    var_counts = np.var(counts)
    Y = (var_counts / mean_counts) - 1  # Feynman-Y statistic
    
    # Create figures
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original time distribution
    ax1.plot(time_values, mean_values, 'b-', linewidth=0.8)
    ax1.scatter(time_values, mean_values, color='b', s=10)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Neutron emission')
    ax1.set_title('Time-correlated Neutron events')
    ax1.grid(True)
    
    # Feynman histogram
    hist, bins, _ = ax2.hist(counts, bins=30, density=True, alpha=0.7)
    ax2.set_xlabel('Counts outcome')
    ax2.set_ylabel('Total counts')
    ax2.set_title(f'Feynman Histogram (Y={Y:.3f})')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('feynman_analysis.png', dpi=300)
    plt.show()

    # Print statistics
    print(f"\nFeynman Analysis Results:")
    print(f"Mean counts per gate: {mean_counts:.2f}")
    print(f"Variance: {var_counts:.2f}")
    print(f"Feynman-Y: {Y:.3f}")

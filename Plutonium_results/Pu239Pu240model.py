import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pu239_concentration = 0.92
pu240_concentration = 1 - pu239_concentration

# Create Cf-252 material
pu_mix = openmc.Material(name='Pu-Mix')
pu_mix.add_nuclide('Pu239', pu239_concentration)
pu_mix.add_nuclide('Pu240', pu240_concentration)
pu_mix.set_density('g/cm3', 19.8)  # Density of plutonium

materials = openmc.Materials([pu_mix])

# Create geometry - small sphere for source
sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
cell = openmc.Cell(fill=pu_mix, region=-sphere)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)

# Energy distribution

pu239_watt = openmc.stats.Watt(a=0.885247, b=3.802690)
pu240_watt = openmc.stats.Watt(a=0.794930, b=4.689270)

lambda_239 = np.log(2)/(24110*365.25*24*3600)  # decay constant in s^-1
lambda_240 = np.log(2)/(6561*365.25*24*3600)   # decay constant in s^-1

total_time = 10  # seconds
# Calculate expected decays for each isotope
expected_decays_239 = 37000 * np.exp(lambda_239 * 31557600) * total_time * pu239_concentration
expected_decays_240 = 37000 * np.exp(lambda_240 * 31557600) * total_time * pu240_concentration
expected_decays = expected_decays_239 + expected_decays_240

source = openmc.IndependentSource()

print("Expected decay", expected_decays)
source.time = openmc.stats.Uniform(0, total_time)
source.angle = openmc.stats.Isotropic()
source.space = openmc.stats.Point((0, 0, 0))
source.energy = openmc.stats.Mixture(
    probability=[pu239_concentration, pu240_concentration],
    distribution=[pu239_watt, pu240_watt]
)
source.particle = "neutron"


# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = int(expected_decays)
settings.source = source

# Create tallies with microsecond time bins
print("Create time bin")
time_bins = np.linspace(0, 10, 10000000)  
time_filter = openmc.TimeFilter(time_bins)

tally = openmc.Tally()
tally.scores = ['flux']
tally.filters = [openmc.CellFilter(cell), time_filter]

tallies = openmc.Tallies([tally])

# Create and run model
print("running model")
model = openmc.model.Model(geometry, materials, settings, tallies)
sp_filename = model.run()

def process_feynman_histogram(time_events, pre_delay = 0, gate_width=2):
    counts_per_gate = []
        
    mean_data = time_events['mean']
    
    windows = np.lib.stride_tricks.sliding_window_view(mean_data[1:], gate_width)
    
    # Sum along axis 1 to get counts per gate
    counts_per_gate = np.sum(windows, axis=1)
    print(len(counts_per_gate))
        
    return counts_per_gate

name = "10sPu239Pu240_095"

# Process results and create graphs
with openmc.StatePoint(sp_filename) as sp:
    tally_result = sp.get_tally()
    df = tally_result.get_pandas_dataframe()

    print(df)
    print(df['mean'].sum())

    # Extract time and mean values
    time_values = df['time low [s]']
    mean_values = df['mean'] * 100000

    event_times = pd.DataFrame({
    'time': time_values,
    'mean': mean_values
    })

    print("events created")
    total_time = 10
    
    # Process using Feynman histogram
# Use range for 16 values (0 to 15) and calculate gate_width as 2^i
y_values = []  # Store Y values for final plot
# Create one big figure with 16 subplots (4x4 grid)
fig = plt.figure(figsize=(20, 20))

num_iterations = 16

for i in range(num_iterations):  # This will give us powers from 2^1 to 2^16
    gate_width = 2 ** (i + 1)  # Start from 2^1 instead of 2^0
    counts = process_feynman_histogram(event_times, gate_width=gate_width)
    counts = counts.round(2)
    
    # Calculate Feynman statistics
    n = len(counts)
    mean = sum(counts) / n
    # Calculate variance
    # Variance is the average of squared differences from the mean
    squared_diff_sum = sum((x - mean) ** 2 for x in counts)
    variance = squared_diff_sum / n
    print(n)
    print(mean)
    print(variance)
    Y = (variance / mean) - 1  # Feynman-Y statistic
    y_values.append(Y)
    
    # Create subplot
    ax = fig.add_subplot(5, 4, i + 1)
    
    # Feynman histogram
    hist, bins, _ = ax.hist(counts, bins=30, density=True, alpha=0.7)
    ax.set_xlabel('Counts outcome')
    ax.set_ylabel('Total counts')
    ax.set_title(f'Gate width={gate_width}\nY={Y:.3f}\nMean={mean:.2f}\nVar={variance:.2f}')
    ax.grid(True)

plt.tight_layout()
plt.savefig(f'{name}{total_time}_all_feynman_histograms.png', dpi=300)
plt.show()

# Create variance/mean vs gate width plot
plt.figure(figsize=(10, 6))
gate_widths = [2 ** (i + 1) for i in range(num_iterations)]  # Calculate all gate widths for plotting
plt.semilogx(gate_widths, y_values, 'bo-')
plt.xlabel('Gate width')
plt.ylabel('Variance/Mean - 1 (Y)')
plt.title('Feynman-Y vs Gate Width')
plt.grid(True)
plt.savefig(f'{name}{total_time}_feynman_Y_vs_gate_width.png', dpi=300)
plt.show()

# Print final statistics
print("\nFeynman Analysis Results for all gate widths:")
for gw, y in zip(gate_widths, y_values):
    print(f"Gate width: {gw:5d}, Feynman-Y: {y:.3f}")
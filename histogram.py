import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def process_feynman_histogram(time_events, pre_delay = 0, gate_width=2):
    counts_per_gate = []
        
    mean_data = time_events['mean']
    
    windows = np.lib.stride_tricks.sliding_window_view(mean_data[1:], gate_width)
    
    # Sum along axis 1 to get counts per gate
    counts_per_gate = np.sum(windows, axis=1)
    print(len(counts_per_gate))
        
    return counts_per_gate

sp_filename = "10s_statepoint.100.h5"

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
gate_width = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216]
y_values = []  # Store Y values for final plot

# Create one big figure with 16 subplots (4x4 grid)
fig = plt.figure(figsize=(20, 20))

for idx, i in enumerate(gate_width, 1):
    counts = process_feynman_histogram(event_times, gate_width=i)
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
    ax = fig.add_subplot(6, 4, idx)
    
    # Feynman histogram
    hist, bins, _ = ax.hist(counts, bins=30, density=True, alpha=0.7)
    ax.set_xlabel('Counts outcome')
    ax.set_ylabel('Total counts')
    ax.set_title(f'Gate width={i}\nY={Y:.3f}\nMean={mean:.2f}\nVar={variance:.2f}')
    ax.grid(True)

plt.tight_layout()
plt.savefig(f'{total_time}_all_feynman_histograms.png', dpi=300)
plt.show()

# Create variance/mean vs gate width plot
plt.figure(figsize=(10, 6))
plt.semilogx(gate_width, y_values, 'bo-')
plt.xlabel('Gate width')
plt.ylabel('Variance/Mean - 1 (Y)')
plt.title('Feynman-Y vs Gate Width')
plt.grid(True)
plt.savefig(f'{total_time}_feynman_Y_vs_gate_width.png', dpi=300)
plt.show()

# Print final statistics
print("\nFeynman Analysis Results for all gate widths:")
for gw, y in zip(gate_width, y_values):
    print(f"Gate width: {gw:5d}, Feynman-Y: {y:.3f}")
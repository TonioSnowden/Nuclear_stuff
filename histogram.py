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
    mean_values = df['mean'] * 1000

    event_times = pd.DataFrame({
    'time': time_values,
    'mean': mean_values
    })

    print("events created")
    total_time = 10
    
    # Process using Feynman histogram
    gate_width = [8192, 16384, 32768]
    for i in gate_width:
        counts = process_feynman_histogram(event_times, gate_width = i)
        
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
        plt.savefig(f'{total_time}_feynman_analysis{i}.png', dpi=300)
        plt.show()
    
        # Print statistics
        print(f"\nFeynman Analysis Results:")
        print(f"Mean counts per gate: {mean_counts:.2f}")
        print(f"Variance: {var_counts:.2f}")
        print(f"Feynman-Y: {Y:.3f}")
import openmc
import numpy as np
import matplotlib.pyplot as plt  # Changed this line
from scipy.stats import gaussian_kde

# Load the tracks file
tracks = openmc.Tracks('tracks.h5')

ax = tracks.plot()
# Assuming you have a 3D plot
fig = ax.figure  # Get the figure from the axes
fig.savefig("tracks.png", dpi='figure', bbox_inches='tight', pad_inches=0.1)

particle_times = []

# Print track data
for track in tracks:
    print(track)
    neutron_track = track.filter(particle='neutron')
    print(neutron_track)
    states = neutron_track.particle_tracks
    for state in states:
        particle_states = state.states  # time in seconds
        time = particle_states["time"]
        particle_times = np.append(particle_times, time)
        print(f"Particle time: {time} seconds")

print(particle_times)
print(len(particle_times))

plt.figure(figsize=(10, 6))
plt.hist(particle_times, bins=50, density=True, alpha=0.7, color='blue')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency')
plt.title('Distribution of Neutron Event Times')

# Add a KDE curve to smooth the distribution
if len(particle_times) > 1:  # KDE requires at least 2 points
    kde = gaussian_kde(particle_times)
    x_range = np.linspace(min(particle_times), max(particle_times), 200)
    plt.plot(x_range, kde(x_range), 'r-', lw=2, label='KDE')
    plt.legend()

plt.grid(True)
plt.savefig("event_histogram.png", dpi=300, bbox_inches='tight')
plt.show()

def count_events_in_gates(time_events, gate_width, total_time=10):
    """
    Count events in consecutive time gates of fixed width.
    
    Args:
        time_events: Array of event times
        gate_width: Width of each time gate
        total_time: Total time period to analyze
    """
    # Create time bins from 0 to total_time with gate_width intervals
    bins = np.arange(0, total_time, gate_width)
    
    # Count events in each bin
    counts, _ = np.histogram(time_events, bins=bins)
    
    return counts

def analyze_feynman_y(time_events, num_iterations=20, total_time=10):
    """
    Perform Feynman analysis for different gate widths.
    """
    y_values = []
    gate_widths = []
    
    # Iterate through different gate widths (powers of 2)
    for i in range(num_iterations):
        gate_width = 2 ** (i + 1)  # Start from 2^1
        gate_width_micro = gate_width / 100000000
        
        # Count events in gates
        counts = count_events_in_gates(time_events, gate_width_micro, total_time)
        
        # Calculate statistics
        mean = np.mean(counts)
        variance = np.var(counts)
        Y = (variance / mean) - 1
        
        y_values.append(Y)
        gate_widths.append(gate_width)
        
    return np.array(gate_widths), np.array(y_values)

def plot_feynman_results(gate_widths, y_values):
    """
    Create the Feynman-Y vs gate width plot.
    """
    plt.figure(figsize=(10, 6))
    plt.semilogx(gate_widths, y_values, 'bo-', linewidth=1.5, markersize=6)
    plt.grid(True)
    plt.xlabel('Gate width')
    plt.ylabel('Variance/Mean - 1 (Y)')
    plt.title('Feynman-Y vs Gate Width')
    return plt.gcf()

# Analyze and plot
gate_widths, y_values = analyze_feynman_y(particle_times)
fig = plot_feynman_results(gate_widths, y_values)
plt.show()
plt.savefig("gate_width_track")

# Print results
print("\nFeynman Analysis Results:")
for gw, y in zip(gate_widths, y_values):
    print(f"Gate width: {gw:5d}, Feynman-Y: {y:.3f}")
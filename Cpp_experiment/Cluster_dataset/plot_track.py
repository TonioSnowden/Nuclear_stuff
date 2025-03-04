import openmc
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import json

# Load parameters from config file
with open('config.json') as config_file:
    config = json.load(config_file)

# Load the tracks file
tracks = openmc.Tracks('tracks.h5')

ax = tracks.plot()
fig = ax.figure  # Get the figure from the axes
fig.savefig("tracks.png", dpi='figure', bbox_inches='tight', pad_inches=0.1)

particle_times = []

# Print track data
for track in tracks:
    neutron_track = track.filter(particle='neutron')
    states = neutron_track.particle_tracks
    for state in states:
        particle_states = state.states  # time in seconds
        time = particle_states["time"]
        particle_times = np.append(particle_times, time)

plt.figure(figsize=(10, 6))
plt.hist(particle_times, bins=config['histogram_bins'], density=True, alpha=0.7, color='blue')  # Bins from config
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

# The rest of the code remains unchanged...
from typing import Any
import openmc
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import json

def get_particle_times() -> np.ndarray:
    # Load parameters from config file
    with open('config.json') as config_file:
        config = json.load(config_file)

    # Load the tracks file
    tracks = openmc.Tracks('tracks.h5')

    ax = tracks.plot()
    fig = ax.figure  # Get the figure from the axes
    fig.savefig("tracks.png", dpi='figure', bbox_inches='tight', pad_inches=0.1)

    particle_times: list[Any] = []

    # Print track data
    for track in tracks:
        neutron_track = track.filter(particle='neutron')
        states = neutron_track.particle_tracks
        for state in states:
            particle_states = state.states  # time in seconds
            time = particle_states["time"]
            particle_times = np.append(particle_times, time)

    return np.array(particle_times)

# Example usage
if __name__ == "__main__":
    times = get_particle_times()
    print(times)
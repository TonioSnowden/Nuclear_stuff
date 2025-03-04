from typing import Any
import openmc
import numpy as np
import sys

def get_particle_times() -> np.ndarray:
    # Load the tracks file
    tracks = openmc.Tracks('tracks.h5')

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

def save_results(density, radius, particles, particle_times):
    with open('particle_times_output.csv', 'a') as f:
        f.write(f"{density},{radius},{particles},{particle_times}\n")

if __name__ == "__main__":
    # Get parameters from command line arguments
    density = sys.argv[1]
    radius = sys.argv[2]
    particles = sys.argv[3]

    particle_times = get_particle_times()

    # Save the results
    save_results(density, radius, particles, particle_times)
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

def save_results(source_file, density, air_density, radius, particle_times):
    # Filter out zero values from particle_times
    non_zero_times = particle_times[particle_times != 0]
    
    with open('particle_times_output.csv', 'a') as f:
        f.write(f"{source_file},{density},{air_density},{radius},{non_zero_times}\n")

if __name__ == "__main__":
    # Get parameters from command line arguments
    source_file = sys.argv[1]
    fuel_density = sys.argv[2]
    coolant_density = sys.argv[3]
    radius = sys.argv[4]

    particle_times = get_particle_times()

    # Save the results
    save_results(source_file, fuel_density, coolant_density, radius, particle_times)
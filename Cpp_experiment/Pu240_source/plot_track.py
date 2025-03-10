from typing import Any
import openmc
import numpy as np
import sys

def main():
    source_file = sys.argv[1]
    fuel_density = sys.argv[2]
    coolant_density = sys.argv[3]
    radius = sys.argv[4]

    tracks = openmc.Tracks('tracks.h5')

    particle_times = []

    for track in tracks:
    neutron_track = track.filter(particle='neutron')
    states = neutron_track.particle_tracks
    for state in states:
        particle_states = state.states  # time in seconds
        time = particle_states["time"]
        particle_times = np.append(particle_times, time)

    particle_times = np.round(np.array(particle_times), decimals=4)

    particle_times_str = np.array2string(
        particle_times,
        separator=',',
        threshold=np.inf,
        precision=4,
        suppress_small=True
    ).replace('\n', '')

    new_data = pd.DataFrame({
        'source_file': [source_file],
        'fuel_density': [round(fuel_density, 4)],
        'coolant_density': [round(coolant_density, 4)],
        'radius': [round(radius, 4)],
        'particle_times': [particle_times_str]
    })
    
    # If file exists, append to it; if not, create new file
    try:
        df = pd.read_csv('particle_times_output.csv')
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    
    # Write to CSV without index
    df.to_csv('particle_times_output.csv', index=False)     

if __name__ == '__main__':
    main()
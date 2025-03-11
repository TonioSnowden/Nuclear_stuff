from typing import Any
import openmc
import numpy as np
import sys
import pandas as pd

def main():
    source_file = sys.argv[1]
    fuel_density = sys.argv[2]
    coolant_density = sys.argv[3]
    radius = sys.argv[4]

    tracks = openmc.Tracks('tracks.h5')

    ax = tracks.plot()
    fig = ax.figure  # Get the figure from the axes
    fig.savefig("tracks.png", dpi='figure', bbox_inches='tight', pad_inches=0.1)

    particle_times = []

    for track in tracks:
        neutron_track = track.filter(particle='neutron')
        states = neutron_track.particle_tracks
        for state in states:
            particle_states = state.states  # time in seconds
            time = particle_states["time"]
            time = np.delete(time, np.where(time == 0))
            particle_times = np.append(particle_times, time)

    print(particle_times)

    new_data = pd.DataFrame({
        'source_file': [source_file],
        'fuel_density': fuel_density,
        'coolant_density': coolant_density,
        'radius': radius,
        'particle_times': [particle_times]
    })
    
    # If file exists, append to it; if not, create new file
    try:
        df = pd.read_csv('particle_times_output.csv')
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    
    # Write to CSV without index
    print(df)
    df.to_csv('particle_times_output.csv', index=False)     

if __name__ == '__main__':
    main()
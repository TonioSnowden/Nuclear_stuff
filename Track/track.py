import openmc
import numpy as np
import

# Load the tracks file
tracks = openmc.Tracks('tracks.h5')

ax = tracks.plot()
# Assuming you have a 3D plot
fig = ax.figure  # Get the figure from the axes
fig.savefig("tracks.png", dpi='figure', bbox_inches='tight', pad_inches=0.1)

# Print track data
for track in tracks:
    print(track)
    neutron_track = track.filter(particle='neutron')
    print(neutron_track)
    states = neutron_track.particle_tracks
    for state in states:
        particle_states = state.states  # time in seconds
        time = particle_states["time"]
        print(f"Particle time: {time} seconds")
import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pu240 = openmc.Material(name='Pu-240')
pu240.add_nuclide('Pu240', 1.0)
pu240.set_density('g/cm3', 19.1)  

air = openmc.Material(name='Air')
air.add_element('N', 0.784)
air.add_element('O', 0.216)
air.set_density('g/cm3', 0.001225)

# Create a box filled with HDPE
x_min, x_max = -10, 10
y_min, y_max = -10, 10
z_min, z_max = -10, 10

left = openmc.XPlane(x_min)
right = openmc.XPlane(x_max)
bottom = openmc.YPlane(y_min)
top = openmc.YPlane(y_max)
front = openmc.ZPlane(z_min)
back = openmc.ZPlane(z_max)

air_box = +left & -right & +bottom & -top & +front & -back
air_cell = openmc.Cell(fill=air, region=air_box)

sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
pu240_cell = openmc.Cell(fill=pu240, region=-sphere)
universe = openmc.Universe(cells=[air_cell, pu240_cell])
geometry = openmc.Geometry(universe)

source_lib = "/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build/libpu240_source.so"

# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = 10  # Adjust based on your needs
settings.source = openmc.CompiledSource(source_lib)

print("Running simulation...")
model = openmc.model.Model(geometry, settings)
sp_filename = model.run()
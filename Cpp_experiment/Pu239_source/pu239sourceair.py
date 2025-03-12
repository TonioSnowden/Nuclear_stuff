import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

with open('config.json') as config_file:
    config = json.load(config_file) 

pu239 = openmc.Material(name='Pu-239')
pu239.add_nuclide('Pu239', 1.0)
pu239.set_density('g/cm3', config['fuel_density'])  

air = openmc.Material(name='Air')
air.add_element('N', 0.784)
air.add_element('O', 0.216)
air.set_density('g/cm3', config['coolant_density'])

# Create a box filled with HDPE
x_min, x_max = -10, 10
y_min, y_max = -10, 10
z_min, z_max = -10, 10

left = openmc.XPlane(x_min, boundary_type='vacuum')
right = openmc.XPlane(x_max, boundary_type='vacuum')
bottom = openmc.YPlane(y_min, boundary_type='vacuum')
top = openmc.YPlane(y_max, boundary_type='vacuum')
front = openmc.ZPlane(z_min, boundary_type='vacuum')
back = openmc.ZPlane(z_max, boundary_type='vacuum')

sphere = openmc.Sphere(r=config['radius'])
box_region = +left & -right & +bottom & -top & +front & -back

# Define the HDPE cell to be the box MINUS the sphere
air_cell = openmc.Cell(fill=air, region=box_region & ~(-sphere))

# Define the Pu-240 cell to be inside the sphere
pu239_cell = openmc.Cell(fill=pu239, region=-sphere)

universe = openmc.Universe(cells=[air_cell, pu239_cell])
geometry = openmc.Geometry(universe)

source_lib = "/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu239_source/build/libpu239_source.so"

# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = 10  # Adjust based on your needs
settings.source = openmc.CompiledSource(source_lib)

print("Running simulation...")
model = openmc.model.Model(geometry=geometry, settings=settings)
sp_filename = model.run()
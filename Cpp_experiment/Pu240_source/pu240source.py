import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pu240 = openmc.Material(name='Pu-240')
pu240.add_nuclide('Pu240', 1.0)
pu240.set_density('g/cm3', 19.1)  

materials = openmc.Materials([pu240])

# Create geometry - small sphere for source
sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
cell = openmc.Cell(fill=pu240, region=-sphere)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)

source_lib = "/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu240_source/build/libpu240_source.so"

# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = 10  # Adjust based on your needs
settings.source = openmc.CompiledSource(source_lib)

print("Running simulation...")
model = openmc.model.Model(geometry, materials, settings)
sp_filename = model.run()
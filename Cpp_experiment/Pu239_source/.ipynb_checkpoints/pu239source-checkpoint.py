import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Create Pu-239 material
pu239 = openmc.Material(name='Pu-239')
pu239.add_nuclide('Pu239', 1.0)
pu239.set_density('g/cm3', 19.1)  # Density of U-238

materials = openmc.Materials([pu239])

# Create geometry - small sphere for source
sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
cell = openmc.Cell(fill=pu239, region=-sphere)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)

source_lib = "/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/Pu239_source/build/libpu239_source.so"

# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = 10  # Adjust based on your needs
settings.source = openmc.CompiledSource(source_lib)

print("Running simulation...")
model = openmc.model.Model(geometry, materials, settings)
sp_filename = model.run()
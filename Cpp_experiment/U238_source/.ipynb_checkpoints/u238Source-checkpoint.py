import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Create U-238 material
u238 = openmc.Material(name='U-238')
u238.add_nuclide('U238', 1.0)
u238.set_density('g/cm3', 19.1)  # Density of U-238

materials = openmc.Materials([u238])

# Create geometry - small sphere for source
sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
cell = openmc.Cell(fill=u238, region=-sphere)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)

source_lib = "/global/scratch/users/toniooppi/Nuclear_stuff/Cpp_experiment/build/libu238_source.so"

# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = 100  # Adjust based on your needs
settings.source = openmc.CompiledSource(source_lib)

print("Running simulation...")
model = openmc.model.Model(geometry, materials, settings)
sp_filename = model.run()
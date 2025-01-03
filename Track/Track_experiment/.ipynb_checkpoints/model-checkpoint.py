import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pu239_concentration = 0.92
pu240_concentration = 1 - pu239_concentration

# Create Cf-252 material
pu_mix = openmc.Material(name='Pu-Mix')
pu_mix.add_nuclide('Pu239', pu239_concentration)
pu_mix.add_nuclide('Pu240', pu240_concentration)
pu_mix.set_density('g/cm3', 19.8)  # Density of plutonium

materials = openmc.Materials([pu_mix])

# Create geometry - small sphere for source
sphere = openmc.Sphere(r=3.0, boundary_type='vacuum')
cell = openmc.Cell(fill=pu_mix, region=-sphere)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)

# Energy distribution

pu239_watt = openmc.stats.Watt(a=0.885247, b=3.802690)
pu240_watt = openmc.stats.Watt(a=0.794930, b=4.689270)

lambda_239 = np.log(2)/(24110*365.25*24*3600)  # decay constant in s^-1
lambda_240 = np.log(2)/(6561*365.25*24*3600)   # decay constant in s^-1

total_time = 10  # seconds
# Calculate expected decays for each isotope
expected_decays_239 = 37000 * np.exp(lambda_239 * 31557600) * total_time * pu239_concentration
expected_decays_240 = 37000 * np.exp(lambda_240 * 31557600) * total_time * pu240_concentration
expected_decays = expected_decays_239 + expected_decays_240

source = openmc.IndependentSource()

print("Expected decay", expected_decays)
source.time = openmc.stats.Uniform(0, total_time)
source.angle = openmc.stats.Isotropic()
source.space = openmc.stats.Point((0, 0, 0))
source.energy = openmc.stats.Uniform(0,1)
source.particle = "neutron"


# Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.batches = 100
settings.particles = int(expected_decays)
settings.source = source

# Create and run model
print("running model")
model = openmc.model.Model(geometry, materials, settings)
sp_filename = model.run()
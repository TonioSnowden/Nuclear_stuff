import openmc
import numpy as np

# Define materials
hdpe = openmc.Material(name='HDPE')
hdpe.add_element('H', 2, percent_type='ao')
hdpe.add_element('C', 1, percent_type='ao')
hdpe.set_density('g/cm3', 0.95)

he3 = openmc.Material(name='He-3')
he3.add_nuclide('He3', 1.0)
he3.set_density('g/cm3', 100)

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

hdpe_box = +left & -right & +bottom & -top & +front & -back
hdpe_cell = openmc.Cell(fill=hdpe, region=hdpe_box)

# Create 4 He-3 tubes inside the box
tube_radius = 1.5
tube_height = 15
tube_positions = [
    (-7.5, 0, 0),
    (-2.5, 0, 0),
    (2.5, 0, 0),
    (7.5, 0, 0)
]

he3_tubes = []
for i, pos in enumerate(tube_positions):
    cylinder = openmc.YCylinder(x0=pos[0], z0=pos[2], r=tube_radius)
    tube_region = -cylinder & +openmc.YPlane(y0=pos[1]-tube_height/2) & -openmc.YPlane(y0=pos[1]+tube_height/2)
    he3_tubes.append(openmc.Cell(fill=he3, region=tube_region))

# Create a cell for the air around the box
outer_box = openmc.rectangular_prism(width=50, height=50, axis='z', origin=(0, 0, 0)) & openmc.ZPlane(z0=-25) & -openmc.ZPlane(z0=25)
air_region = outer_box & ~box_region
for tube in he3_tubes:
    air_region = air_region & ~tube.region
air_cell = openmc.Cell(fill=air, region=air_region)

# Create the geometry
geometry = openmc.Geometry([hdpe_cell] + he3_tubes + [air_cell])

# Create Cf-252 source
source = openmc.Source()
source.space = openmc.stats.Point((0, 0, 15))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Watt(a=1.025, b=2.926)  # Cf-252 spectrum
source.particle = 'neutron'

# Create settings
settings = openmc.Settings()
settings.batches = 100
settings.inactive = 10
settings.particles = 10000
settings.source = source

# Create tallies for He-3 tubes
tallies = openmc.Tallies()
for i, tube in enumerate(he3_tubes):
    tally = openmc.Tally(name=f'He3_tube_{i+1}')
    tally.scores = ['absorption']
    tally.filters = [openmc.CellFilter(tube)]
    tallies.append(tally)

# Create and run the model
model = openmc.Model(geometry=geometry, settings=settings, tallies=tallies)
model.run()
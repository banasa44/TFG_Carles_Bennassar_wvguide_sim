from app import constants, setup
import math
import numpy as np
import matplotlib.pyplot as plt
import meep as mp


resolution=20

filename = "_%d_%d_%03d_%03d"
#inicialització de les simulacions
sim_xy = mp.Simulation(cell_size = setup.Grid.cell_xy,
                    boundary_layers = constants.pml_layers ,
                    geometry = setup.Grid.geometry_xy ,
                    sources= setup.Source.source_xy ,
                    resolution=resolution,
                    default_material=constants.materials['water'])

sim_xz = mp.Simulation(cell_size = setup.Grid.cell_xz,
                    boundary_layers = constants.pml_layers ,
                    geometry = setup.Grid.geometry_xz ,
                    sources= setup.Source.source_xz ,
                    resolution=resolution,
                    default_material=constants.materials['air'] )

sim_rot = mp.Simulation(cell_size = setup.Grid.cell_xz,
                    boundary_layers = constants.pml_layers ,
                    geometry = setup.Grid.geometry_xz ,
                    sources= setup.Source.source_rot ,
                    resolution=resolution,                    
                    default_material=constants.materials['air'],
                    k_point=setup.k)

#funció per a fer correr les diferents simulacions
#paràmetres: (simulació a usar, temps que es vol fer correr la simulació, quina cel·la es farà servir
def simulation (simulation, until, cell):
    simulation.run(until=until)
    eps_data = simulation.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
    ez_data = simulation.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
    return ez_data, eps_data

#inicialització dels diferents plots (components del camp i estructura)
ez_data, eps_data= simulation(sim_xz, 100, setup.Grid.cell_xz)
#print(ez_data, np.real(ez_data))
ez_data=np.real(ez_data)
eps_data=np.real(eps_data)

ez_data1, eps_data1= simulation(sim_rot, 100, setup.Grid.cell_xz)
#print(ez_data, np.real(ez_data))
ez_data1=np.real(ez_data1)
eps_data1=np.real(eps_data1)

plt.figure('Ez')
plt.subplot(211)
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)


plt.subplot(212)
plt.imshow(ez_data1.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
plt.show()

'''
fig=plt.figure('EPS')
ax = fig.add_subplot(1, 1, 1)
major_ticks = np.arange(0, 700, 10)
minor_ticks = np.arange(0, 700, 2)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)
plt.imshow(eps_data1.transpose(), interpolation='spline36', cmap='RdBu')
plt.show()
'''
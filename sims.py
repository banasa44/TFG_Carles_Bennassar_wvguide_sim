from app import constants, setup
import math
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

theta_src=20
resolution=20
k = mp.Vector3(math.cos(theta_src),math.sin(theta_src),0)
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
                    k_point=k,
                    default_material=constants.materials['air'] )

#funció per a fer correr les diferents simulacions
#paràmetres: (simulació a usar, temps que es vol fer correr la simulació, quina cel·la es farà servir
def simulation (simulation, until, cell):
    simulation.run(until=until)
    eps_data = simulation.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
    ez_data = simulation.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
    return ez_data, eps_data

#inicialització dels diferents plots (components del camp i estructura)
ez_data, eps_data= simulation(sim_xz, 100, setup.Grid.cell_xz)

plt.figure('Ez')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
#plt.axis('off')
plt.savefig('Ez_field'+filename+'_xzrrr'+'nm.png')
plt.show()

plt.figure('EPS')
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='RdBu')
#plt.axis('off')
plt.savefig('Ez_field'+filename+'_xzrrr_0nm.png')
plt.show()

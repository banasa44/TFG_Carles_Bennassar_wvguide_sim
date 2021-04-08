from app import constants, setup 
from app.constants import Wave, Sizes
from app.setup import Grid, Source, Detectors
import math
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

theta_src=20
resolution=20
k = mp.Vector3(math.cos(theta_src),math.sin(theta_src),0)
filename = "_%d_%d_%03d_%03d"
#inicialització de les simulacions
sim_xy = mp.Simulation(cell_size = Grid.cell_xy,
                    boundary_layers = constants.pml_layers ,
                    geometry = Grid.geometry_xy ,
                    sources= Source.source_xy ,
                    resolution=resolution,
                    default_material=constants.materials['water'])

sim_xz = mp.Simulation(cell_size = Grid.cell_xz,
                    boundary_layers = constants.pml_layers ,
                    geometry = Grid.geometry_xz ,
                    sources= Source.source_xz ,
                    resolution=resolution,
                    default_material=constants.materials['air'] )
'''
sim_rot = mp.Simulation(cell_size = Grid.cell_xz,
                    boundary_layers = constants.pml_layers ,
                    geometry = Grid.geometry_xz ,
                    sources= Source.source_rot ,
                    resolution=resolution,
                    k_point=k,
                    default_material=constants.materials['air'] )
'''
#funció per a fer correr les diferents simulacions
#paràmetres: (simulació a usar, temps que es vol fer correr la simulació, quina cel·la es farà servir
def simulation (sim, cell, **simrun_args):
    det = Detectors( center=mp.Vector3(-4.25,0,0),size=mp.Vector3(0,5.0,0))
    direct = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det.direct_fr)
    tran = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det.tran_fr)
    sim.run(**simrun_args)
    eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
    ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
    flux_freqs = mp.get_flux_freqs(direct)
    direct_data = mp.get_fluxes(direct)
    tran_data = mp.get_fluxes(tran)
    return eps_data, ez_data, flux_freqs, direct_data, tran_data
'''
sim = sim_xy

direct_fr = mp.FluxRegion(center=mp.Vector3(-4.0, 0, 0), size=mp.Vector3( 0,Sizes.block_y/2,0))  
tran_fr = mp.FluxRegion(center=mp.Vector3(Sizes.num_blocks*Sizes.alpha/2, 0, 0), size=mp.Vector3(0, Sizes.block_y/2,0))

direct = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, direct_fr)
tran = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, tran_fr)

sim.run(until=100)

eps_data = sim.get_array(center=mp.Vector3(), size=Grid.cell_xy, component=mp.Dielectric)
ez_data = sim.get_array(center=mp.Vector3(), size=Grid.cell_xy, component=mp.Ez)

flux_freqs = mp.get_flux_freqs(direct)
direct_data = mp.get_fluxes(direct)
tran_data = mp.get_fluxes(tran)
'''
eps_data,ez_data, flux_freqs, direct_data, tran_data = simulation(sim_xy, Grid.cell_xy, until=200)
                                                      


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


wl = []
Ds = []
Ts = []
for i in range(Wave.nfreq):
    wl = np.append(wl, 1/flux_freqs[i])
    Ds = np.append(Ds, direct_data[i])
    Ts = np.append(Ts, tran_data[i]/direct_data[i])    


plt.figure('Transmission')
plt.plot(wl,Ds,'bo-',label='direct beam')
plt.plot(wl,Ts,'ro-',label='transmitance')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.show()

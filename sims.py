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
def sim_ini (cell, geometry, source, resolution, bckg):
    return mp.Simulation(cell_size = cell,
                    boundary_layers = constants.pml_layers ,
                    geometry = geometry ,
                    sources= source ,
                    resolution=resolution,
                    default_material=bckg)

#funció per a fer correr les diferents simulacions
#paràmetres: (simulació a usar, temps que es vol fer correr la simulació, quina cel·la es farà servir
def simulation (sim, cell, **simrun_args):
    #inicialitzo els dos detectors (a les diferents posicions)
    det_dir = Detectors(center=mp.Vector3(-4.25,0,0),size=mp.Vector3(0,5.0,0))
    det_tran = Detectors(center=mp.Vector3(3.25,0,0),size=mp.Vector3(0,5.0,0))
    #afegeixo els fluxos
    direct = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det_dir.detect_fr)
    tran = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det_tran.detect_fr)
    sim.run(**simrun_args)
    #prenc les dades per fer els dibuixos
    eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
    ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
    #prenc les dades per fer les gràfiques
    flux_freqs = mp.get_flux_freqs(direct)
    direct_data = mp.get_fluxes(direct)
    tran_data = mp.get_fluxes(tran)
    return eps_data, ez_data, flux_freqs, direct_data, tran_data

# aquí faig la simulació en blanc, i guardo les dades "blanques"
sim_white = sim_ini(Grid.cell_xy, [],Source.source_xy,20,constants.materials['water'])
eps_white_data, ez_white_data, flux_white_freqs, direct_white_data, tran_white_data = simulation(sim_white, Grid.cell_xy, until=200)

# aquí faig la simulació amb tots els blocs, i guardo les dades de la graella
sim_xy = sim_ini(Grid.cell_xy, Grid.geometry_xy, Source.source_xy,20,constants.materials['water'])
eps_data,ez_data, flux_freqs, direct_xy_data, tran_xy_data = simulation(sim_xy, Grid.cell_xy, until=200)
                                                      


plt.figure('Ez')
plt.subplot(311)
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
#plt.axis('off')
#plt.savefig('Ez_field'+filename+'_xzrrr'+'nm.png')
#plt.show()

plt.subplot(312)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='RdBu')
#plt.axis('off')
#plt.savefig('Ez_field'+filename+'_xzrrr_0nm.png')
#plt.show()


wl = []
Ds = []
Ts = []
#aquí guardo les dades dels fluxos per a plotejar-les, agafo de tot les white_data menys de la transmesa
#que agafo la tran_xy_data/direct_white_data
for i in range(Wave.nfreq):
    wl = np.append(wl, 1/flux_white_freqs[i])
    Ds = np.append(Ds, direct_white_data[i])
    Ts = np.append(Ts, tran_xy_data[i]/direct_white_data[i])    


plt.subplot(313)
plt.plot(wl,Ds,'bo-',label='direct beam')
plt.plot(wl,Ts,'ro-',label='transmitance')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.show()

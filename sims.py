from app import constants, setup 
from app.constants import Wave, Sizes
from app.setup import Grid, Source, Detectors, k
import math
import numpy as np
import matplotlib.pyplot as plt
import meep as mp


resolution=20

filename = "_%d_%d_%03d_%03d"
#inicialització de les simulacions
def sim_ini (cell, geometry, source, resolution, kpoint, bckg):
    return mp.Simulation(cell_size = cell,
                    boundary_layers = constants.pml_layers ,
                    geometry = geometry ,
                    sources= source ,
                    resolution=resolution,
                    k_point = kpoint,
                    default_material=bckg)

#funció per a fer correr les diferents simulacions
#paràmetres: (simulació a usar, temps que es vol fer correr la simulació, quina cel·la es farà servir
def simulation (sim, cell,det_dir,det_tran, **simrun_args):
    #inicialitzo els dos detectors (a les diferents posicions)
    det_dir = det_dir       #Detectors(center=mp.Vector3(-4.25,0,0),size=mp.Vector3(0,5.0,0))
    det_tran = det_tran     #Detectors(center=mp.Vector3(3.25,0,0),size=mp.Vector3(0,5.0,0))
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

#inicialitzo els detectors que vulgui posar
det_dir = Detectors(
        center=mp.Vector3(-(constants.Sizes.alpha*constants.Sizes.num_blocks/2)+0.5,0,0),
        size=mp.Vector3(0,5.0,0))
det_tran = Detectors(
        center=mp.Vector3((constants.Sizes.alpha*constants.Sizes.num_blocks/2)-0.15,0,0),
        size=mp.Vector3(0,5.0,0))

# aquí faig la simulació en blanc, i guardo les dades "blanques"
sim_white = sim_ini(
                cell=Grid.cell_xy,
                geometry=[],
                source=Source.source_xy,
                resolution=20,
                kpoint=None,
                bckg=constants.materials['water'])
eps_white_data, ez_white_data, flux_white_freqs, direct_white_data, tran_white_data = simulation(
                                                                                            sim=sim_white, 
                                                                                            cell=Grid.cell_xy,
                                                                                            det_dir=det_dir,
                                                                                            det_tran=det_tran,
                                                                                            until=200)

# aquí faig la simulació amb tots els blocs, i guardo les dades de la graella
sim = sim_ini(
            cell=Grid.cell_xy,
            geometry=Grid.geometry_xy,
            source=Source.source_rot,
            resolution=20,
            kpoint=k,
            bckg=constants.materials['water'])
eps_data, ez_data, flux_freqs, direct_data, tran_data = simulation(
                                                        sim=sim, 
                                                        cell=Grid.cell_xy,
                                                        det_dir=det_dir,
                                                        det_tran=det_tran,
                                                        until=200)
#converteixo les dades del camp en valors reals per a poder-los plotejar                                                      
ez_data=np.real(ez_data)
eps_data=np.real(eps_data)

#PLOTS
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

#aquí guardo les dades dels fluxos per a plotejar-les, agafo de tot les white_data menys de la transmesa
#que agafo la tran_xy_data/direct_white_data
wl = []
Ds = []
Ts = []
for i in range(Wave.nfreq):
    wl = np.append(wl, 1/flux_white_freqs[i])
    Ds = np.append(Ds, direct_white_data[i]/direct_white_data[i])
    Ts = np.append(Ts, tran_data[i]/direct_white_data[i])    


plt.subplot(313)
plt.plot(wl,Ds,'bo-',label='direct beam')
plt.plot(wl,Ts,'ro-',label='transmitance')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.show()
plt.savefig('simple_grid_w_'+str(constants.Sizes.block_x)+'_nm.png')

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
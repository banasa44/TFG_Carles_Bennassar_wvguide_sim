from app import constants, setup 
from app.constants import Wave, Sizes
from app.setup import Grid, Source, Detectors, k
import math
import numpy as np
import matplotlib.pyplot as plt
import meep as mp


resolution=20

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
def simulation (sim, cell,det_dir,det_tran, det_tran_2,**simrun_args):
    #inicialitzo els dos detectors (a les diferents posicions)
    det_dir = det_dir       #Detectors(center=mp.Vector3(-4.25,0,0),size=mp.Vector3(0,5.0,0))
    det_tran = det_tran     #Detectors(center=mp.Vector3(3.25,0,0),size=mp.Vector3(0,5.0,0))
    det_tran_2 = det_tran_2
    #afegeixo els fluxos
    direct = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det_dir.detect_fr)
    tran = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det_tran.detect_fr)
    tran_2 = sim.add_flux(Wave.fcen, Wave.df, Wave.nfreq, det_tran_2.detect_fr)
    sim.run(**simrun_args)
    #prenc les dades per fer els dibuixos
    eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
    ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
    #prenc les dades per fer les gràfiques
    flux_freqs = mp.get_flux_freqs(direct)
    direct_data = mp.get_fluxes(direct)
    tran_data = mp.get_fluxes(tran)
    tran_data_2= mp.get_fluxes(tran_2)
    reset=sim.reset_meep()
    return eps_data, ez_data, flux_freqs, direct_data, tran_data,tran_data_2,reset

#inicialitzo els detectors que vulgui posar
det_dir = Detectors(
        center=mp.Vector3(-(Sizes.alpha*Sizes.num_blocks/4),-0.68,0),
        size=mp.Vector3(6.0,0,0),
        direction=mp.Y)
det_tran = Detectors(
        center=mp.Vector3((Sizes.alpha*Sizes.num_blocks/2)-0.75,0,0),
        size=mp.Vector3(0,0.3,0),
        direction=mp.X)
det_tran_2 = Detectors(
        center=mp.Vector3((Sizes.alpha*Sizes.num_blocks/2)-0.25,2.0,0),
        size=mp.Vector3(0.0,1.5,0),
        direction=mp.X)

# aquí faig la simulació en blanc, i guardo les dades "blanques"
sim_white = sim_ini(
                cell=Grid.cell_xz,
                geometry=[],
                source=Source.source_xz,
                resolution=20,
                kpoint=None,
                bckg=constants.materials['air'])
eps_white_data, ez_white_data, flux_white_freqs, direct_white_data, tran_white_data, tran_white_data_2,reset = simulation(
                                                                                            sim=sim_white, 
                                                                                            cell=Grid.cell_xz,
                                                                                            det_dir=det_dir,
                                                                                            det_tran=det_tran,
                                                                                            det_tran_2=det_tran_2,
                                                                                            until=200)
reset
# aquí faig la simulació amb tots els blocs, i guardo les dades de la graella
sim = sim_ini(
            cell=Grid.cell_xz,
            geometry=Grid.geometry_xz,
            source=Source.source_rot,
            resolution=20,
            kpoint=k,
            bckg=constants.materials['air'])
eps_data, ez_data, flux_freqs, direct_data, tran_data ,tran_data_2,reset= simulation(
                                                        sim=sim, 
                                                        cell=Grid.cell_xz,
                                                        det_dir=det_dir,
                                                        det_tran=det_tran,
                                                        det_tran_2=det_tran_2,
                                                        until = 2000)
                                                        #until_after_sources = mp.stop_when_fields_decayed(50, mp.Ez, 
                                                        #mp.Vector3((constants.Sizes.alpha*constants.Sizes.num_blocks/2)-0.15,Sizes.height_si/2,0), 1e-6))
#converteixo les dades del camp en valors reals per a poder-los plotejar                                                      

ez_data=np.real(ez_data)
eps_data=np.real(eps_data)


#PLOTS
plt.figure('Ez')
plt.title('Simulation rays for XZ')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
plt.axis('on')
#plt.savefig('app/static/images/sim/simple_grid_sim_w_'+str(constants.Sizes.block_x)+'alph_'+str(Sizes.alpha)+', R='+str(Sizes.R)+'μm.png')
#plt.show()

plt.figure('fff')
plt.title('Simulation grid for XZ')
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='RdBu')
#plt.axis('off')

#plt.show()

#aquí guardo les dades dels fluxos per a plotejar-les, agafo de tot les white_data menys de la transmesa
#que agafo la tran_xy_data/direct_white_data
wl = []
Ds = []
Ts = []
Ts_2 = []
for i in range(Wave.nfreq):
    wl.append(1/flux_white_freqs[i])
    Ds.append(direct_white_data[i]/direct_white_data[i])
    Ts.append(tran_data[i]/direct_white_data[i])
    Ts_2.append(tran_data_2[i]/direct_white_data[i])    



plt.figure('Graph')
plt.title('Transmitance normalized to gaussian source: XZ')
plt.plot(wl,Ds,'bo-',label='direct beam')
plt.plot(wl,Ts,'ro-',label='transmitance')
plt.plot(wl,Ts_2,'go-',label='transmitance 2')
#plt.plot(wl,1-Ds-Ts,'go-',label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.ylabel("transmitance")
plt.legend(loc="best")
#plt.savefig('app/static/images/graph/simple_grid_w_'+str(constants.Sizes.block_x)+'alph_'+str(Sizes.alpha)+', R='+str(Sizes.R)+'μm.png')
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
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='RdBu')
plt.show()
'''
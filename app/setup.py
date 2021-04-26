import meep as mp
from app import constants 
from app.constants import Sizes
import numpy as np
import math
import cmath


class Grid ():
    cell_xy = mp.Vector3( Sizes.cell_size_x, Sizes.cell_size_y,0)
    cell_xz = mp.Vector3( Sizes.cell_size_x,  Sizes.cell_size_z,0)
    pos_ini_x=Sizes.cell_size_x/2-Sizes.pml_size
    pos_ini_y=Sizes.cell_size_y/2-Sizes.pml_size
    pos_ini_z=Sizes.cell_size_z/2-Sizes.pml_size

# blocks de silici en el plà XY equiespaiats
    geometry_xy=[]
    for i in np.arange(0, Sizes.num_blocks*Sizes.alpha, Sizes.alpha): #arange (0,4,1) --> i = 0 1 2 3  
        geometry_xy.append(mp.Block(
            size= mp.Vector3(Sizes.block_x, Sizes.block_y,0),
            center = mp.Vector3( -(pos_ini_x-Sizes.block_x/2)+i, 0, 0),  
            material = constants.materials['si']) )        
        
#blocks de silici en el plà XZ equiespaiats + block antireflexant de SiO2 + capa d'aire
    geometry_xz = []
    for i in np.arange(0, Sizes.num_blocks*Sizes.alpha, Sizes.alpha):  
        geometry_xz.append( mp.Block(
            size= mp.Vector3(Sizes.block_x,  Sizes.block_z, 0),
            center = mp.Vector3( -(pos_ini_x-Sizes.block_x/2)+i,
            -Sizes.block_z/2, 0),
            material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_si, Sizes.height_si, 0),
        center = mp.Vector3( 0, Sizes.height_si/2, 0), 
        material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_sio2, Sizes.height_sio2, 0),
        center = mp.Vector3( 0, Sizes.height_si+ Sizes.height_sio2/2, 0),
        material = constants.materials['sio2']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_si, Sizes.height_sio2*2, 0),
        center = mp.Vector3( 0, Sizes.height_sio2*2, 0), 
        material = constants.materials['si']))

'''
    geometry_xy = []    
    for i in np.arange(0, Sizes.num_blocks*Sizes.alpha, Sizes.alpha): #arange (0,4,1) --> i = 0 1 2 3  
        geometry_xy.append( mp.Block(
            size= mp.Vector3(Sizes.alpha*(Sizes.F_0-Sizes.R*i), Sizes.block_y,0),
            center = mp.Vector3( -(pos_ini_x-Sizes.block_x/2)+i, 0, 0),           
            material = constants.materials['si']))
        

#blocks de silici en el plà XZ equiespaiats + block antireflexant de SiO2 + capa d'aire
    geometry_xz = []
    for i in np.arange(0, Sizes.num_blocks*Sizes.alpha, Sizes.alpha):  
        geometry_xz.append( mp.Block(
            size= mp.Vector3(Sizes.alpha*(Sizes.F_0-Sizes.R*i),  Sizes.block_z, 0),
            center = mp.Vector3( -(pos_ini_x-Sizes.block_x/2)+i,
            -Sizes.block_z/2, 0),
            material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_si, Sizes.height_si, 0),
        center = mp.Vector3( 0, Sizes.height_si/2, 0), 
        material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_sio2, Sizes.height_sio2, 0),
        center = mp.Vector3( 0, Sizes.height_si+ Sizes.height_sio2/2, 0),
        material = constants.materials['sio2']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_si, Sizes.height_sio2*2, 0),
        center = mp.Vector3( 0, Sizes.height_sio2*2, 0), 
        material = constants.materials['si']))
   geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_si, Sizes.height_si*2, 0),
        center = mp.Vector3( 0, Sizes.height_si*2+Sizes.height_sio2, 0), 
        material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(Sizes.width_si, Sizes.height_si*2+4, 0),
        center = mp.Vector3( 0, -(Sizes.height_si*2+Sizes.height_sio2+1), 0), 
        material = constants.materials['air']))
'''

theta_src = 0
theta_r = math.radians(theta_src)
# pw-amp is a function that returns the amplitude exp(ik(x+x0)) at a
# given point x.  (We need the x0 because current amplitude functions
# in Meep are defined relative to the center of the current source,
# whereas we want a fixed origin.)  Actually, it is a function of k
# and x0 that returns a function of x ...
def pw_amp(k, x0):
    def _pw_amp(x):
        return cmath.exp(1j*2*math.pi*k.dot(x+x0))
    return _pw_amp

k = mp.Vector3(math.cos(theta_src),math.sin(theta_src),0).scale(constants.Wave.fcen)
if theta_src == 0:
    k = mp.Vector3(0,0,0)

class Source ():
    source_xy = [mp.Source(
        mp.GaussianSource(constants.Wave.fcen,fwidth=constants.Wave.df),
        #mp.ContinuousSource(frequency= constants.Wave.f_max),
        component=mp.Ez,
        center = constants.Sizes.src_center_xy,
        size = constants.Sizes.src_size_xy,
        )]
    source_xz = [mp.Source(
        mp.GaussianSource(constants.Wave.fcen,fwidth=constants.Wave.df),
        #mp.ContinuousSource(frequency= constants.Wave.f_max),
        component = mp.Ez,
        center = constants.Sizes.src_center_xz,
        size = constants.Sizes.src_size_xz,
        )]
    source_rot = [mp.Source(
        mp.GaussianSource(constants.Wave.fcen,fwidth=constants.Wave.df),
        #mp.ContinuousSource(frequency= constants.Wave.f_max),
        component=mp.Ez,
        center = constants.Sizes.src_center_xy,
        size = constants.Sizes.src_size_xy,
        amp_func=pw_amp(k,constants.Sizes.src_center_xy)#(k, mp.Vector3(-Sizes.num_blocks*Sizes.alpha/2, 0, 0))
    )]
class Detectors (object):
    def __init__(self,center,size):
        # direct flux
        self.detect_fr = mp.FluxRegion(center = center, size = size)    
import meep as mp
from app import constants
import numpy as np
import math
import cmath

rot_theta = math.radians(30)
theta_src=20
resolution=20
k = mp.Vector3(math.cos(theta_src),math.sin(theta_src),0)

class Grid ():
    cell_xy = mp.Vector3( constants.sizes['v1']['cell_size_x'], constants.sizes['v1']['cell_size_y'],0)
    cell_xz = mp.Vector3( constants.sizes['v1']['cell_size_x'],  constants.sizes['v1']['cell_size_z'],0)
    pos_ini_x=constants.sizes['v1']['cell_size_x']/2-constants.sizes['v1']['pml_size']
    pos_ini_y=constants.sizes['v1']['cell_size_y']/2-constants.sizes['v1']['pml_size']
    pos_ini_z=constants.sizes['v1']['cell_size_z']/2-constants.sizes['v1']['pml_size']

# blocks de silici en el plà XY equiespaiats
    geometry_xy = []
    for i in np.arange(0, constants.sizes['v1']['num_blocks'], constants.sizes['v1']['alpha']): #arange (0,4,1) --> i = 0 1 2 3  
        geometry_xy.append( mp.Block(
            size= mp.Vector3(constants.sizes['v1']['block_width_si'], constants.sizes['v1']['block_length_si'],0),
            center = mp.Vector3( -pos_ini_x+constants.sizes['v1']['block_width_si']/2+i, 0, 0),
            #per a rotar blocks
            #e1=mp.Vector3(1,0,0).rotate(mp.Vector3(0,0,1),rot_theta),
            #e2=mp.Vector3(0,1,0).rotate(mp.Vector3(0,0,1),rot_theta),            
            material = constants.materials['si']))

#blocks de silici en el plà XZ equiespaiats + block antireflexant de SiO2 + capa d'aire
    geometry_xz = []
    for i in np.arange(0, constants.sizes['v1']['num_blocks'], constants.sizes['v1']['alpha']):  
        geometry_xz.append( mp.Block(
            size= mp.Vector3(constants.sizes['v1']['block_width_si'],  constants.sizes['v1']['block_height_si'], 0),
            center = mp.Vector3( -(pos_ini_x-constants.sizes['v1']['block_width_si']/2)+i,
            -constants.sizes['v1']['block_height_si']/2, 0),
            material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(constants.sizes['v1']['width_si'], constants.sizes['v1']['height_si'], 0),
        center = mp.Vector3( 0, constants.sizes['v1']['height_si']/2, 0), 
        material = constants.materials['si']))
    geometry_xz.append( mp.Block(
        size= mp.Vector3(constants.sizes['v1']['width_sio2'], constants.sizes['v1']['height_sio2'], 0),
        center = mp.Vector3( 0, constants.sizes['v1']['height_si']+ constants.sizes['v1']['height_sio2']/2, 0),
        material = constants.materials['sio2']))
    '''geometry_xz.append( mp.Block(
        size= mp.Vector3(constants.sizes['v1']['width_air'], constants.sizes['v1']['height_air'], 0),
        center = mp.Vector3( 0, -constants.sizes['v1']['height_air']/2, 0),
        material = constants.materials['air']))'''
    geometry_xz.append( mp.Block(
        size= mp.Vector3(constants.sizes['v1']['width_si'], constants.sizes['v1']['height_si']*2+4, 0),
        center = mp.Vector3( 0, constants.sizes['v1']['height_si']*2+constants.sizes['v1']['height_sio2']+2, 0), 
        material = constants.materials['si']))



class Source ():
    source_xy = [mp.Source(
        mp.ContinuousSource(frequency= constants.Wave.f_max),
        component=mp.Ez,
        center= mp.Vector3(-4.5,0,0))]
    source_xz = [mp.Source(
        mp.ContinuousSource(frequency= constants.Wave.f_max),
        component = mp.Ez,
        center = mp.Vector3(-1.5, -1, 0),
        size = mp.Vector3(6,0,0),
        )]

    source_rot = [mp.Source(mp.GaussianSource(constants.Wave.fcen,fwidth=constants.Wave.df),
                       component=mp.Ez,
                       center=mp.Vector3(-4.25, -1, 0),
                       size=mp.Vector3(3,0,0),
                       amp_func=cmath.exp(1j*2*math.pi*k.dot(mp.Vector3(-4.25, -1, 0))))]

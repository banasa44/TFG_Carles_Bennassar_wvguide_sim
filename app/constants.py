''' ALL CONSTANTS OF THE PROJECT DEFINED IN LISTS'''

import meep as mp

# diccionari amb els índex de refracció dels diferents materials
materials = {
    "air":mp.Medium(index= 1.0), 
    'si': mp.Medium(index= 3.47),
    'xxx': mp.Medium(index= 8.47),
    'water': mp.Medium(index= 1.33),
    'sio2': mp.Medium(index= 1.44)
}
#tamany dels PML
pml_layers = [mp.PML(1.0)]

#paràmetres necessaris per a descriure les ones EM que usaré
class Wave ():
    wavelength_max = 1550
    wavelength_min = 1330
    f_max = 1000/wavelength_min
    f_min = 1000/wavelength_max
    df = f_max - f_min
    fcen = (f_max+f_min)/2
    nfreq = wavelength_max-wavelength_min


#mides dels diferents layers i blocks que es faran servir
class Sizes ():
 #versió espaiat constant
    version = 'continous alpha and l_o and l_e'
    l_e= 0.5
    num_blocks = 24
    pml_size = 1.0
    #0.43 --- 0.46   0.47 no
    #TODO
    block_x = 0.6
    #TODO
    block_y = 8.0
    block_z = 0.16
    block_x_min = 0.3
    block_x_max = 0.6

    alpha = 1.1
    F_0=0.9
    R=0.025
    
    width_si = num_blocks*alpha
    height_si = 0.1
    width_sio2 = num_blocks*alpha
    height_sio2 = 1.0
    width_air = num_blocks*alpha
    height_air = 1.5
    
    cell_size_x = num_blocks*alpha + 2.0*pml_size
    cell_size_y = block_y + 2.0*pml_size
    cell_size_z = 7.0

    src_center_xy = mp.Vector3(-(alpha*num_blocks/2)-0.15,0,0)
    #src_center_xz = mp.Vector3(-(alpha*num_blocks/2)+3,-1,0)
    src_center_xz = mp.Vector3(1.5,-2,0)
    src_size_xy = mp.Vector3(0,6,0)
    src_size_xz = mp.Vector3(6,0,0)

#versió = x.0
'''
    l_e= 0.5
    num_blocks = 18
    pml_size = 1.0
    
    block_x = 0.54
    block_y = 8.0
    block_z = 0.16
    alpha = 0.6
    F_0=0.9
    R=0.025
    
    width_si = num_blocks*alpha
    height_si = 0.1
    width_sio2 = num_blocks*alpha
    height_sio2 = 1.0
    width_air = num_blocks*alpha
    height_air = 1.5
    
    cell_size_x = num_blocks*alpha + 2.0*pml_size
    cell_size_y = block_y + 2.0*pml_size
    cell_size_z = 7.0
    src_center_xy = mp.Vector3(-(alpha*num_blocks/2)-0.31,0,0)
    #src_center_xz = mp.Vector3(-(alpha*num_blocks/2)+3,-1,0)
    src_center_xz = mp.Vector3(1.5,-2,0)
    src_size_xy = mp.Vector3(0,6,0)
    src_size_xz = mp.Vector3(6,0,0)
'''  
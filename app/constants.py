''' ALL CONSTANTS OF THE PROJECT DEFINED IN LISTS'''

import meep as mp

# diccionari amb els índex de refracció dels diferents materials
materials = {
    "air":mp.Medium(index= 1.0), 
    'si': mp.Medium(index= 3.45),
    'water': mp.Medium(index= 1.33),
    'sio2': mp.Medium(index= 1.45)
}
#tamany dels PML
pml_layers = [mp.PML(2.0)]

#paràmetres necessaris per a descriure les ones EM que usaré
class Wave ():
    wavelength_max = 1.55
    f_max = 1/wavelength_max
    wavelength_min = 1.33
    f_min = 1/wavelength_min
    df = f_max - f_min
    fcen = (f_max+f_min)/2

#mides dels diferents layers i blocks que es faran servir

class Sizes ():
    alpha = 1.0
    num_blocks = 8.0
    pml_size = 2.0
    width_si = 8.0
    height_si = 0.5
    block_x = 0.5
    block_y = 6.0
    block_z = 0.5
    width_sio2 = 8.0
    height_sio2 = 1.0
    width_air = 8.0
    height_air = 1.5
    cell_size_x = num_blocks*alpha + 2*pml_size
    cell_size_y = block_y + 2.0
    cell_size_z = 7.0



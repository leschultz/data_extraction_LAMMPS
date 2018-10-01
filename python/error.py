from diffusionimport import load
from diffusionerrorplot import error

import numpy as np


path = '/home/nerve/Desktop/motion_curves/datacalculated/diffusion/'
run = 'uw4000atom345000_boxside-22_hold1-80000_hold2-5000_hold3-45000_timestep-0p001_dumprate-500_2000K-1350K_run1_origins_1350'

name = path+run

data = load(name)
print(error(data['all']))

from diffusionimport import load

import numpy as np

def variance(x):
    '''
    Determine the error between values.
    '''

    N = len(x)

    var = 0
    for i in range(0, N):
        for j in range(i+1, N):
            var += (x[i]-x[j])**2

    var /= N**2

    return var

path = '/home/nerve/Desktop/motion_curves/datacalculated/diffusion/'
run = 'uw4000atom345000_boxside-22_hold1-80000_hold2-5000_hold3-45000_timestep-0p001_dumprate-500_2000K-1350K_run1_origins_1350'

name = path+run

data = load(name)
print(variance(data['all']))
print(np.std(data['all'])**2)
print(np.std(data['all']))
print(np.var(data['all'])**.5)

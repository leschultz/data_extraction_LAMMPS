from scipy import stats as st
from itertools import islice

import numpy as np


def load(name):
    '''
    This function loads the diffusion data from multiple origins.
    '''

    # Save the headers from the data file
    with open(name) as file:
        for line in islice(file, 0, 1):
            header = line.strip().split(',')

    # Crate a dictionary to store lists of values
    data = {}
    for head in header:
        data[head] = []

    # Save the data for diffusion
    with open(name) as file:
        next(file)
        for line in file:
            value = line.strip().split(',')
            value = [float(i) for i in value]

            count = 0
            for item in value:
                data[header[count]].append(value[count])
                count += 1

    # Return all diffusivity data
    return data


def diffusion(data):
    '''
    Propagate error from the standard error of atomic positions.
    '''

    time = data['time']

    del data['time']

    diff = {}
    for key in data:
        if '_EIM' not in key:
            upper = np.array(data[key])+np.array(data[key+'_EIM'])
            lower = np.array(data[key])-np.array(data[key+'_EIM'])

            upper = list(upper)
            lower = list(lower)

            up = st.linregress(time, upper)
            lo = st.linregress(time, lower)

            diffup = up[0]/6
            diffdo = lo[0]/6

            diff[key+'_err'] = diffup-diffdo

    return diff

path = '/home/nerve/Desktop/motion_curves/datacalculated/msd/'
run = 'Al100Sm0_boxside-10_hold1-100000_hold2-237500_hold3-500000_timestep-0p001_dumprate-100_2000K-385K_run1'

name = path+run

data = load(name)
print(diffusion(data))

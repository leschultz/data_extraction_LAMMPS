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
            header = line.strip().split(' ')

    # Crate a dictionary to store lists of values
    data = {}
    for head in header:
        data[head] = []

    # Save the data for diffusion
    with open(name) as file:
        next(file)
        for line in file:
            value = line.strip().split(' ')
            value = [float(i) for i in value]

            count = 0
            for item in value:
                data[header[count]].append(value[count])
                count += 1

    # Return all diffusivity data
    return data


def block_averaging(data):
    '''
    Devides the data into ten portions do do block averaging.
    '''

    N = 10  # Number of blocks
    length = len(data['start_time'])  # The data length
    half = length//10  # Divide indexes but removes point if remainder exists

    blocks = list(range(0, length, half))  # Index intervals

    # Filter the data
    del data['start_time']

    # The following delete lines are temporary
    delete = []
    for key in data:
        if '_Err' in key:
            delete.append(key)

    for key in delete:
        del data[key]

    block_data = {}
    for key in data:
        count = 0
        for block in blocks[:-1]:
            start = blocks[count]
            end = blocks[count+1]

            name = key+'_'+str(count)
            block_data[name] = data[key][start:end]

            count += 1

    averages = []
    count = 0
    for key in block_data:
        averages.append(np.mean(block_data[key]))

        count += 1

    diffusion = np.mean(averages)
    diffusion_eim = st.sem(averages)

    return diffusion, diffusion_eim

path = '/home/nerve/Desktop/motion_curves/datacalculated/diffusion/'
run = 'Al100Sm0_boxside-10_hold1-100000_hold2-237500_hold3-500000_timestep-0p001_dumprate-100_2000K-385K_run1_origins'

name = path+run

data = load(name)
print(block_averaging(data))

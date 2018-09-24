from itertools import islice

import numpy as np


def load(name):
    '''
    This function loads the diffusion data from multiple origins.
    '''

    with open(name) as file:
        for line in islice(file, 0, 1):
            header = line.strip().split(' ')

    data = {}
    for head in header:
        data[head] = []

    with open(name) as file:
        next(file)
        for line in file:
            value = line.strip().split(' ')
            value = [float(i) for i in value]

            count = 0
            for item in value:
                data[header[count]].append(value[count])
                count += 1

    return data


def covariance(x):
    '''
    Determine the covariaance from thermodynamic equilibrium.
    '''

    length = len(x)-1
    average = np.mean(x)

    cov = 0
    for i in range(0, length):
        cov += x[i]*x[i+1]-average**2

    cov /= length

    return cov


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
run = 'Al100Sm0_boxside-10_hold1-100000_hold2-137500_hold3-500000_timestep-0p001_dumprate-100_2000K-1065K_run1_origins'

name = path+run

data = load(name)
print(variance(data['all']))
print(np.var(data['all']))

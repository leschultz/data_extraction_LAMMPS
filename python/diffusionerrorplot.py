from atom_error_propagation import diffusion as di
from block_averaging import block_averaging as bl
from matplotlib import pyplot as pl
from diffusionimport import load
from scipy import stats as st

import pandas as pd
import numpy as np
import os


def error(x):
    '''
    Error calculation by Van de Wall.
    '''

    L = len(x)
    mean = np.mean(x)

    V = 0
    for i in range(0, L):
        for j in range(0, L):
            l = abs(i-j)

            q = 0
            for k in range(0, L-l):
                q += x[k]*x[k+l]-mean**2

            q /= (L-l)

            V += q

    V /= L**2
    V **= 0.5

    return V


directory = '../datacalculated/diffusion/'

runs = os.listdir(directory)

diffusion = {}
diffusion['scipy'] = []
diffusion['block'] = []
diffusion['sem'] = []
differr = {}
differr['scipy'] = []
differr['block'] = []
differr['fit'] = []
differr['sem'] = []
differr['VandeWall'] = []

temp = []
temp2 = []
for run in runs:

    if '_origins' not in run:

        temp.append(int(run.split('run1_')[1]))

        with open(directory+run) as file:
            next(file)
            for line in file:
                value = line.strip().split(',')
                diffusion['scipy'].append(float(value[0]))
                differr['scipy'].append(float(value[1]))

    if '_origins' in run:

        word = run.split('run1_')[1]
        number = int(word.split('_')[1])
        temp2.append(number)

        data = load(directory+run, ' ')
        block = bl(data)
        diffusion['block'].append(block['all'])
        differr['block'].append(block['all_err'])

        diffusion['sem'].append(np.mean(data['all']))
        differr['sem'].append(st.sem(data['all']))

        differr['VandeWall'].append(error(data['all']))

directory = '../datacalculated/msd/'

runs = os.listdir(directory)

for run in runs:
    data = load(directory+run, ',')
    atom = di(data)
    differr['fit'].append(atom['all_err'])

pl.plot(temp, differr['scipy'], '.', label='Slope Fitting')
pl.plot(temp2, differr['block'], '.', label='Block Avg (n=10)')
pl.plot(temp2, differr['sem'], '.', label='EIM Scipy')
pl.plot(temp, differr['fit'], '.', label='MSD Bounds')
pl.plot(temp, differr['VandeWall'], '.', label='Van de Wall')

pl.xlabel('Temperature [K]')
pl.ylabel('Error [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.show()

print(differr['VandeWall'])

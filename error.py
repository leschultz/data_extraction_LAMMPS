from atom_error_propagation import diffusion as di
from block_averaging import block_averaging as bl
from autocorrelation import standarderror as er
from matplotlib import pyplot as pl
from diffusionimport import load
from scipy import stats as st

from actualldiffusion import actual

import numpy as np
import os

maindir = '../export/'
directory = maindir+'4000atom545000/datacalculated/diffusion/'

runs = os.listdir(directory)

diffusion = {}
diffusion['block'] = []
differr = {}
differr['block'] = []

temp = []
temp2 = []
for run in runs:

    if '_origins' in run:

        word = run.split('_')[1]
        number = int(word[:-1])
        temp2.append(number)

        data = load(directory+run, ' ')
        block = bl(data)
        diffusion['block'].append(block['all'])
        differr['block'].append(block['all_err'])

real = actual("/home/nerve/Desktop/export")
x = []
y = []
for key in real:
    if 'err' not in str(key):
        x.append(key)
        y.append(real[str(key)+'_err'])

pl.plot(x, y, '.', label='Actual Standard Error (10 runs)')

pl.plot(temp2, differr['block'], '.', label='Block Avg (n=10)')

pl.xlabel('Temperature [K]')
pl.ylabel('Error [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.show()

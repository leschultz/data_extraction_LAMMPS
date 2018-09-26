from atom_error_propagation import diffusion as di
from block_averaging import block_averaging as bl
from matplotlib import pyplot as pl
from diffusionimport import load
from scipy import stats as st

import pandas as pd
import numpy as np
import os

directory = '../datacalculated/diffusion/'

runs = os.listdir(directory)

diffusion = {}
diffusion['scipy'] = []
diffusion['block'] = []
diffusion['var'] = []
differr = {}
differr['scipy'] = []
differr['block'] = []
differr['fit'] = []
differr['var'] = []

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
        number = int(word.split('K_')[0])
        temp2.append(1350-number)

        data = load(directory+run, ' ')
        block = bl(data)
        diffusion['block'].append(block['all'])
        differr['block'].append(block['all_err'])

        diffusion['var'].append(np.mean(data['all']))
        differr['var'].append(st.sem(data['all']))
        print(diffusion['var'])

directory = '../datacalculated/msd/'

runs = os.listdir(directory)

for run in runs:
    data = load(directory+run, ',')
    atom = di(data)
    differr['fit'].append(atom['all_err'])

fig, axs = pl.subplots(2, 2)

axs[0, 0].errorbar(
                   temp,
                   diffusion['scipy'],
                   differr['scipy'],
                   marker='.',
                   linestyle='None',
                   ecolor='r'
                   )

axs[1, 0].errorbar(
                   temp,
                   diffusion['scipy'],
                   differr['fit'],
                   marker='.',
                   linestyle='None',
                   ecolor='r'
                   )

axs[0, 1].errorbar(
                   temp2,
                   diffusion['block'],
                   differr['block'],
                   marker='.',
                   linestyle='None',
                   ecolor='r'
                   )

axs[1, 1].errorbar(
                   temp2,
                   diffusion['var'],
                   differr['var'],
                   marker='.',
                   linestyle='None',
                   ecolor='r'
                   )


pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion [*10^-4 cm^2 s^-1]')
pl.grid(b=True, which='both')
pl.tight_layout()
pl.show()
#pl.savefig('../images/diffusion/diffusion_v_temp_scipy')
pl.clf()


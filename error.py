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

folders = os.listdir(maindir)

paths = {}
for folder in folders:
    paths[maindir+folder+'/datacalculated/diffusion/'] = {}

megadata = {}
for folder in paths:

    runs =  os.listdir(folder)

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
            if megadata.get(number) is None:
                megadata[number] = []

            data = load(folder+run, ' ')

            megadata[number].append(data)
            block = bl(data)
            diffusion['block'].append(block['all'])
            differr['block'].append(block['all_err'])

    paths[folder] = {
                     'temp': temp2,
                     'block': diffusion['block'],
                     'block_err': differr['block']
                     }

megablock = {}
for key in megadata:
    megablock[key] = {
                      'start_time': [],
                      'all': [],
                      'all_Err': [],
                      '1': [],
                      '1_Err': []
                      }

for key in megadata:
    count = 0
    for item in megadata[key]:
        for key2 in item:
            megablock[key][key2] += megadata[key][count][key2]
        count += 1

temp3 = []
newdata = {}
for key in megablock:
    temp3.append(key)
    block = bl(megablock[key])
    newdata[key] = block

blocks = []
blockserr = []
for key in paths:
    print(key)
    print(paths[key]['block'])
    blocks.append(paths[key]['block'])
    blockserr.append(paths[key]['block_err'])

blockmean = np.mean(blockserr, axis=0)
blockmeanerr = st.sem(blockserr, axis=0)

real = actual("/home/nerve/Desktop/export")
x = []
y = []
for key in real:
    if 'err' not in str(key):
        x.append(key)
        y.append(real[str(key)+'_err'])


pl.plot(x, y, '.', label='Actual Standard Error (10 runs)')

pl.errorbar(temp2, blockmean, blockmeanerr, marker='.', linestyle='None', label='Block Avg (n=10)')

for key in newdata:
    pl.plot(key, newdata[key]['all_err'], 'b.')

pl.xlabel('Temperature [K]')
pl.ylabel('Error [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.show()

from atom_error_propagation import diffusion as di
from block_averaging import block_averaging as bl
from autocorrelation import standarderror as er
from matplotlib import pyplot as pl
from diffusionimport import load
from scipy import stats as st
from itertools import islice

from actualldiffusion import actual

import numpy as np
import os


def errorcomparison(maindir):
    folders = os.listdir(maindir)

    data = {}
    for folder in folders:
        data[folder] = {}

        filepath = maindir+folder+'/datacalculated/diffusion/'
        files = os.listdir(filepath)

        origins = [filepath+i for i in files if 'origin' in i]
        regular = [filepath+i for i in files if 'origin' not in i]

        data[folder]['path'] = filepath
        data[folder]['origins'] = origins
        data[folder]['regular'] = regular

    origins = {}
    regular = {}
    for key in data:
        for item in data[key]:
            if 'origins' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-2]
                    loaded = load(name)
                    block = bl(loaded)

                    if origins.get(temp) is None:
                        origins[temp] = {}

                    for i in block:
                        if origins[temp].get(i) is None:
                            origins[temp][i] = []

                        origins[temp][i].append(block[i])
            if 'regular' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-1]
                    with open(name) as file:
                        for line in islice(file, 0, 1):
                            header = line.strip().split(' ')

                    with open(name) as file:
                        for line in islice(file, 1, None):
                            value = line.strip().split(' ')
                            value = [float(i) for i in value]

                    if regular.get(temp) is None:
                        regular[temp] = {}

                    count = 0
                    for head in header:
                        if regular[temp].get(head) is None:
                            regular[temp][head] = None
                        regular[temp][head] = value[count]
                        count += 1

    return regular, origins

real = actual("/home/nerve/Desktop/export")
x = []
y = []
for key in real:
    if 'err' not in str(key):
        x.append(key)
        y.append(real[str(key)+'_err'])


pl.plot(x, y, '.', label='Actual Standard Error (10 runs)')

pl.xlabel('Temperature [K]')
pl.ylabel('Error [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
# pl.show()

errorcomparison('../export/')

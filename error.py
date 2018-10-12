from block_averaging import block_averaging as bl
from matplotlib import pyplot as pl
from scipy import stats as st

from autocorrelation import *

from diffusionimport import load
from matplotlib import lines
from itertools import islice

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

    regular = {}  # Save the single diffusivity values
    blockorigins = {}  # Save the block method applied to multiple origins
    megablock = {}  # Save all the multiple origins data
    correlationformula = {}  # Errors from correlation formula wrote
    for key in data:
        for item in data[key]:
            if 'origins' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-2]
                    temp = float(temp[:-1])
                    loaded = load(name)
                    block = bl(loaded)

                    if correlationformula.get(temp) is None:
                        correlationformula[temp] = {}

                    for i in loaded:
                        if correlationformula[temp].get(i) is None:
                            correlationformula[temp][i] = []

                        lout, values, lcut = correlationlength(loaded[i])
                        val = standarderror(loaded[i], lcut)

                        correlationformula[temp][i].append(val)

                    if blockorigins.get(temp) is None:
                        blockorigins[temp] = {}

                    for i in block:
                        if blockorigins[temp].get(i) is None:
                            blockorigins[temp][i] = []

                        blockorigins[temp][i].append(block[i])

                    if megablock.get(temp) is None:
                        megablock[temp] = {}

                    for i in loaded:
                        if megablock[temp].get(i) is None:
                            megablock[temp][i] = []

                        megablock[temp][i] += loaded[i]

            if 'regular' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-1]
                    temp = float(temp[:-1])
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
                            regular[temp][head] = []
                        regular[temp][head].append(value[count])
                        count += 1
    blocked = {}
    for temp in megablock:
        block = bl(megablock[temp])
        blocked[temp] = block

    return regular, blockorigins, blocked, correlationformula


regular, blockorigins, megablock, correlationformula = errorcomparison('../export/')

# Gather the standard error from actual runs
for temp in regular:
    for item in regular[temp]:
        if 'all' == item:
            pl.plot(temp, st.sem(regular[temp][item]), 'b.')

# Gather the standard error from block error averages
for temp in blockorigins:
    for item in blockorigins[temp]:
        if 'all' == item:
            pl.plot(temp, st.sem(blockorigins[temp][item]), 'r*')

# Gather the block error from all runs combined into larege dataset
for temp in megablock:
    for item in megablock[temp]:
        if 'all_err' == item:
            pl.plot(temp, megablock[temp][item], 'vk')

# Gather the mean of the standard error given by block method
for temp in blockorigins:
    for item in blockorigins[temp]:
        if 'all_err' in item:
            pl.errorbar(
                        temp,
                        np.mean(blockorigins[temp][item]),
                        st.sem(blockorigins[temp][item]),
                        marker='x',
                        color='g',
                        ecolor='g',
                        linestyle='None'
                        )

'''
# Use the autocorrelation function to determine error
for temp in correlationformula:
    for item in correlationformula[temp]:
        if 'all' == item:
            for i in correlationformula[temp][item]:
                pl.plot(temp, i, '^m')
'''

actual = lines.Line2D(
                      [],
                      [],
                      color='blue',
                      marker='.',
                      linestyle='None',
                      markersize=8,
                      label='SEM 10 Runs'
                      )

spread = lines.Line2D(
                      [],
                      [],
                      color='red',
                      marker='.',
                      linestyle='None',
                      markersize=8,
                      label='Spread for 10 Runs'
                      )

blocksem = lines.Line2D(
                        [],
                        [],
                        color='red',
                        marker='*',
                        linestyle='None',
                        markersize=8,
                        label='SEM Blocks (N=10)'
                        )

blockerr = lines.Line2D(
                        [],
                        [],
                        color='green',
                        marker='x',
                        linestyle='None',
                        markersize=8,
                        label='Blocks SEM Average (N=10)'
                        )

mega = lines.Line2D(
                    [],
                    [],
                    color='black',
                    marker='v',
                    linestyle='None',
                    markersize=8,
                    label='Block Method on All Multiple Origins'
                    )

corr = lines.Line2D(
                    [],
                    [],
                    color='magenta',
                    marker='^',
                    linestyle='None',
                    markersize=8,
                    label='Using the autocorrelation function'
                    )

plotlables = [actual, blocksem, blockerr, mega, corr]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlables, loc='best')
pl.grid()
pl.savefig('../errorcomparison')
pl.clf()

# Gather the standard error from block error averages
for temp in blockorigins:
    for item in blockorigins[temp]:
        if 'all_err' == item:
            for run in blockorigins[temp][item]:
                pl.plot(temp, run, 'r.')


for temp in regular:
    for item in regular[temp]:
        if 'all' == item:
            pl.plot(temp, st.sem(regular[temp][item]), 'b.')

plotlables = [actual, spread]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.grid()
pl.legend(handles=plotlables, loc='best')
pl.savefig('../blockspread')
pl.clf()

from matplotlib import pyplot as pl
from block_averaging import block
from scipy import stats as st

from diffusionimport import load
from matplotlib import lines
from itertools import islice

from autocorrelation import *

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

        data[folder]['origins'] = origins
        data[folder]['regular'] = regular

    regular = {}  # Save the single diffusivity values
    multiple = {}  # Save for multiple origins
    for key in data:
        for item in data[key]:
            if 'origins' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-2]
                    temp = float(temp[:-1])
                    loaded = load(name)

                    if multiple.get(temp) is None:
                        multiple[temp] = {}

                    for i in loaded:
                        if multiple[temp].get(i) is None:
                            multiple[temp][i] = []

                        multiple[temp][i].append(loaded[i])

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

    return regular, multiple 


def regularblock(regular):
    data = {}
    for temp in regular:
        data[temp] = {}
        for key in regular[temp]:
            if 'rr' not in key:
                data[temp][key] = block(regular[temp][key])

    return data


def multipleblock(multiple):
    data = {}
    for temp in multiple:
        data[temp] = {}
        for key in multiple[temp]:
            if 'rr' not in key:
                data[temp][key] = [block(i) for i in multiple[temp][key]]

    return data

regular, multiple = errorcomparison('../export/')
blockedruns = regularblock(regular)

temps = []
averages = []
error = []
for temp in regular:
    temps.append(temp)
    averages.append(np.mean(regular[temp]['all']))
    error.append(st.sem(regular[temp]['all']))

pl.plot(temps, error, 'ob')

temps = []
blockedaverages = []
blockederror = []
for temp in blockedruns:
    temps.append(temp)
    blockedaverages.append(blockedruns[temp]['all'][0])
    blockederror.append(blockedruns[temp]['all'][1])

pl.plot(temps, blockederror, '.r')

temps = []
autoerror = []
for temp in regular:
    temps.append(temp)
    autoerror.append(standarderror(regular[temp]['all'], 0))

pl.plot(temps, autoerror, '*y')

temps = []
autoerror = []
for temp in regular:
    temps.append(temp)
    lout, values, lcut = correlationlength(regular[temp]['all'])
    autoerror.append(standarderror(regular[temp]['all'], lcut))

pl.plot(temps, autoerror, 'xk')

regularval = lines.Line2D(
                         [],
                         [],
                         color='blue',
                         marker='o',
                         linestyle='None',
                         markersize=8,
                         label='Scipy SEM'
                         )

regularblocks = lines.Line2D(
                             [],
                             [],
                             color='red',
                             marker='.',
                             linestyle='None',
                             markersize=8,
                             label='10 Block Averaging SEM'
                             )

autocorrelation0 = lines.Line2D(
                                [],
                                [],
                                color='y',
                                marker='*',
                                linestyle='None',
                                markersize=8,
                                label='Autocorrelation (l=0)'
                                )

autocorrelation = lines.Line2D(
                               [],
                               [],
                               color='k',
                               marker='x',
                               linestyle='None',
                               markersize=8,
                               label='Autocorrelation (l=lcut)'
                               )

plotlables = [regularval, regularblocks, autocorrelation0, autocorrelation]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlables, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../errorcheck')
pl.clf()

origins = multipleblock(multiple)

temps = list(origins.keys())

runs = {}
for temp in origins:
    count = 0
    for item in origins[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        runs[count].append(item[1])
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'b.')

runs = {}
for temp in multiple:
    count = 0
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        runs[count].append(st.sem(item))
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'rx')

one = lines.Line2D(
                   [],
                   [],
                   color='b',
                   marker='.',
                   linestyle='None',
                   markersize=8,
                   label='Block Averaging (n=10) SEM'
                   )

two = lines.Line2D(
                   [],
                   [],
                   color='r',
                   marker='x',
                   linestyle='None',
                   markersize=8,
                   label='Scipy SEM'
                   )

plotlabels = [one, two]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlabels, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../blockvsscipy')
pl.clf()

runs = {}
for temp in multiple:
    count = 0
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        lout, values, lcut = correlationlength(item)
        runs[count].append(standarderror(item, lcut))
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'b.')

runs = {}
for temp in multiple:
    count = 0
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        runs[count].append(st.sem(item))
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'rx')

one = lines.Line2D(
                   [],
                   [],
                   color='b',
                   marker='.',
                   linestyle='None',
                   markersize=8,
                   label='Autocorrelation (l=lcut)'
                   )

two = lines.Line2D(
                   [],
                   [],
                   color='r',
                   marker='x',
                   linestyle='None',
                   markersize=8,
                   label='Scipy SEM'
                   )

plotlabels = [one, two]


pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlabels, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../autovsscipy')
pl.clf()

runs = {}
for temp in multiple:
    if runs.get(temp) is None:
        runs[temp] = []
    for item in multiple[temp]['all']:
        runs[temp] += item

temps = []
megablock = []
autocorr = []
scipysem = []
for temp in runs:
    temps.append(temp)
    megablock.append(block(runs[temp])[1])
    lout, values, lcut = correlationlength(runs[temp])
    print(lcut)
    autocorr.append(standarderror(runs[temp], lcut))
    scipysem.append(st.sem(runs[temp]))

pl.plot(temps, megablock, 'b.', label='Block Average for All')
pl.plot(temps, scipysem, '*k', label='Autoccorrelation for All')
pl.plot(temps, scipysem, 'rx', label='Scipy SEM for All')

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../megaset')
pl.show()
pl.clf()

from matplotlib import pyplot as pl
from scipy import stats as st

from diffusionimport import load
from matplotlib import lines
from itertools import islice

from asymptoticvariance import error as asymp
from stationary import error as standarderror
from batchmeans import error as block
from autocoverr import error as new
from autocovariance import auto

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


ddof = 1
regular, multiple = errorcomparison('../export/')

# Apply methods to single runs
temps = []
averages = []
error = []
autoerror = []
blockedaverages = []
blockederror = []
for temp in regular:
    temps.append(temp)
    averages.append(np.mean(regular[temp]['all']))

    error.append(st.sem(regular[temp]['all'], ddof=ddof))

    autoerror.append(standarderror(regular[temp]['all'])[0])

    bl = block(regular[temp]['all'])
    blockederror.append(bl)

pl.plot(temps, error, 'ob', markerfacecolor='none', markersize=12)
pl.plot(temps, autoerror, 'xk', markerfacecolor='none', markersize=12)
pl.plot(temps, blockederror, '.r', markersize=10)

regularval = lines.Line2D(
                         [],
                         [],
                         color='blue',
                         marker='o',
                         linestyle='None',
                         markersize=8,
                         markerfacecolor='none',
                         label='Scipy SEM'
                         )

regularblocks = lines.Line2D(
                             [],
                             [],
                             color='red',
                             marker='.',
                             linestyle='None',
                             markersize=8,
                             label='Block Averaging'
                             )

autocorrelation = lines.Line2D(
                               [],
                               [],
                               color='k',
                               marker='x',
                               linestyle='None',
                               markersize=8,
                               label='Correlation'
                               )

plotlables = [regularval, regularblocks, autocorrelation]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlables, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../errorcheck')
pl.clf()

# Apply methods to Multiple Origins
temps = []
runsblock = {}
runsscipy = {}
runsauto = {}
for temp in multiple:
    count = 0
    temps.append(temp)
    for item in multiple[temp]['all']:
        if runsblock.get(count) is None:
            runsblock[count] = []
            runsscipy[count] = []
            runsauto[count] = []

        runsblock[count].append(block(item))
        runsscipy[count].append(st.sem(item, ddof=ddof))

        runsauto[count].append(standarderror(item)[0])

        count += 1

for run in runsblock:
    pl.plot(temps, runsblock[0], 'b.')
    pl.plot(temps, runsscipy[0], 'rx')
    pl.plot(temps, runsauto[0], 'yo', markerfacecolor='none')

one = lines.Line2D(
                   [],
                   [],
                   color='b',
                   marker='.',
                   linestyle='None',
                   markersize=8,
                   label='Block Averaging'
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

three = lines.Line2D(
                     [],
                     [],
                     color='y',
                     marker='o',
                     linestyle='None',
                     markersize=8,
                     label='Correlation',
                     markerfacecolor='none'
                     )

plotlabels = [one, two, three]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlabels, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../comparisonsmulti')
pl.clf()

# Apply methods to multiple origins together
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
blockdiff = []
actualldiff = []
for temp in runs:
    temps.append(temp)

    res = block(runs[temp])
    megablock.append(res)

    autocorr.append(standarderror(runs[temp])[0])

    scipysem.append(st.sem(runs[temp]))

pl.plot(temps, megablock, 'b.', label='Block Average for All')
pl.plot(temps, autocorr, '*k', label='Correlation for All')
pl.plot(temps, scipysem, 'rx', label='Scipy SEM for All')

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../megaset')
pl.clf()

from matplotlib import pyplot as pl
from scipy import stats as st

from diffusionimport import load
from matplotlib import lines
from itertools import islice

from ukuiestimator import error as ukui
from batchmeans import error as batch

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

# Apply methods to Multiple Origins
temps = []
runsbatch5 = {}
runsbatch10 = {}
runsukui = {}
runsscipy = {}
for temp in multiple:
    count = 0
    temps.append(temp)
    for item in multiple[temp]['all']:
        if runsscipy.get(count) is None:
            runsbatch5[count] = []
            runsbatch10[count] = []
            runsukui[count] = []
            runsscipy[count] = []

        runsbatch5[count].append(batch(item, 5))
        runsbatch10[count].append(batch(item, 10))
        runsukui[count].append(ukui(item))
        runsscipy[count].append(st.sem(item, ddof=ddof))

        count += 1

batch5label = lines.Line2D(
                           [],
                           [],
                           color='b',
                           marker='.',
                           linestyle='None',
                           markersize=8,
                           label='Batch Means (a=5)'
                           )

batch10label = lines.Line2D(
                            [],
                            [],
                            color='r',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (a=10)'
                            )

ukuilabel = lines.Line2D(
                         [],
                         [],
                         color='y',
                         marker='+',
                         linestyle='None',
                         markersize=8,
                         label='Ukui Estimator',
                         markerfacecolor='none'
                         )

scipylabel = lines.Line2D(
                          [],
                          [],
                          color='k',
                          marker='x',
                          linestyle='None',
                          markersize=8,
                          label='Scipy SEM',
                          markerfacecolor='none'
                          )

plotlabels = [batch5label, batch10label, ukuilabel, scipylabel]

for run in runsscipy:
    pl.plot(temps, runsbatch5[run], 'b.')
    pl.plot(temps, runsbatch10[run], 'r.')
    pl.plot(temps, runsukui[run], 'y+')
    pl.plot(temps, runsscipy[run], 'kx')

    pl.xlabel('Temperature [K]')
    pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
    pl.legend(handles=plotlabels, loc='best')
    pl.grid()
    pl.tight_layout()
    pl.savefig('../'+str(run))
    pl.clf()

print(multiple)

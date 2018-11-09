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

regular, multiple = errorcomparison('../export/')

runs = {}
for temp in multiple:
    if runs.get(temp) is None:
        runs[temp] = []
    for item in multiple[temp]['all']:
        runs[temp] += item

for temp in multiple:
    for run in multiple[temp]['all']:
        k, r, last = auto(run)

        pl.plot(k, r)
    pl.xlabel('Lag-k')
    pl.ylabel('Autocorrelation for temp='+str(temp)+' [K]')
    pl.grid()
    pl.tight_layout()
    pl.savefig('../autocorrelationplot'+str(temp)+'.png')
    pl.clf()

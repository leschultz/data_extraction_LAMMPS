from PyQt5 import QtGui  # Added to be able to import ovito
from matplotlib import pyplot as pl
from scipy import stats as st
from averages import avg

import pandas as pd
import os
import re

# Directories
firstdir = os.getcwd()
lammpstrjdir = firstdir+'/../data/lammpstrj/'

# Grab the file names from the lammpstrj directory
names = os.listdir(lammpstrjdir)

# Grab the names of runs to be averaged
count = 0
for name in names:
    names[count] = name.split('_run')[0]
    count += 1

# Remove repeated items
runs = list(set(names))

for item in runs:

    string = 'Starting multiple time lengths for diffusion'
    print('+'*len(string))
    print(string)
    print('+'*len(string))

    # Parameters from the naming convention
    value = item.split('_')
    system = value[0]
    side = value[1].split('-')[1]
    hold1 = int(value[2].split('-')[1])
    hold2 = int(value[3].split('-')[1])
    hold3 = int(value[4].split('-')[1])
    dumprate = int(value[6].split('-')[1])
    inittemp = int(value[7].split('K-')[0])
    finaltemp = int(value[7].split('K-')[1][:-1])

    timestep = ''
    ptimestep = value[5].split('-')[1]
    for letter in ptimestep:
        if letter == 'p':
            letter = '.'
        timestep += letter

    timestep = float(timestep)

    # Grab the MSD for N points
    N = 10
    newhold3 = []
    for i in range(hold3//N, hold3+1, hold3//N):
        newhold3.append(i)

    # Gather the MSD data for different time lengths
    timediff = {}
    diffusiontime = []
    for hold in newhold3:

        printtext = 'Time used for diffusion: '+str(hold*timestep)+' [ps]'
        print('='*len(printtext))
        print(printtext)
        print('='*len(printtext))

        points = [hold1, hold1+hold2, hold1+hold2+hold]

        # Do averaging for files
        time, msd, diffusion = avg(
                                   item,
                                   points[1],
                                   points[2],
                                   timestep,
                                   dumprate,
                                   [points[0], points[1], points[2]],
                                   10,
                                   50
                                   )

        # The length of time used for diffusion
        diffusiontime.append(hold*timestep)

        # Grab diffusion values for each averaged for different times
        for key in diffusion:

            if timediff.get(key) is None:
                timediff[key] = []

            timediff[key].append(diffusion[key])

    fmt = ''
    nh = ''
    for key in timediff:

        fmt += '%f '
        nh += key+' '

        if 'EIM' not in key:
            pl.errorbar(
                        diffusiontime,
                        timediff[key],
                        yerr=timediff[key+'_EIM'],
                        linestyle='dotted',
                        marker='.',
                        label=key
                        )

    pl.xlabel('Time [ps]')
    pl.ylabel('Diffusion [*10^-4 cm^2 s^-1]')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.legend(loc='best')
    pl.savefig('../images/averaged/diffusion/'+item+'_multi')
    pl.clf()

    output = '../datacalculated/diffusion/'+item+'_multi'

    df = pd.DataFrame(data=timediff)
    df.insert(0, 'time', diffusiontime)

    df.to_csv(output, sep=' ', index=False)

    for key in timediff:

        if 'EIM' not in key:
            pl.errorbar(
                        diffusiontime,
                        timediff[key],
                        yerr=st.sem(timediff[key]),
                        linestyle='dotted',
                        marker='.',
                        label=key
                        )

    pl.xlabel('Time [ps]')
    pl.ylabel('Diffusion [*10^-4 cm^2 s^-1]')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.legend(loc='best')
    pl.savefig('../images/averaged/diffusion/'+item+'_EIMmulti')
    pl.clf()

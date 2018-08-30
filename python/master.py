from PyQt5 import QtGui  # Added to be able to import ovito
from diffusion import diffusion
from averages import avg

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

    # Do averaging for files
    avg(
        item,
        hold1+hold2,
        hold1+hold2+hold3,
        timestep,
        dumprate,
        [hold1, hold1+hold2, hold1+hold2+hold3],
        10,
        50,
        )

    # Grab diffusion with maximum number of points
    diffusion(item, 0, int(hold3/dumprate)+1)

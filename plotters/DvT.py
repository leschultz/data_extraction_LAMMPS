'''
This script plots a diffusion curve for each run that has diffusion
values calculated.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
from importers.infoparser import parameters

from matplotlib import pyplot as pl

import pandas as pd

import argparse
import logging
import glob
import os

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='LAMMPS Runs Directory')
parser.add_argument('-o', help='Analysis Output Directory')
args = parser.parse_args()

# Setup a logging file
formating = (
             '%(asctime)s - ' +
             '%(name)s - ' +
             '%(levelname)s - ' +
             '%(message)s'
             )

logging.basicConfig(
                    filename=args.o+'/overview.log',
                    format=formating
                    )

runs = os.listdir(args.o)
runs = [i for i in runs if '.log' not in i]
runs = [i for i in runs if '.zip' not in i]

# Grab Tg for each run
for run in runs:

    data = {}
    dfiles = []
    path = os.path.join(args.o, run)  # Get run directory

    # Find the diffusion files
    for filename in glob.iglob(path+'/**/*K', recursive=True):
        if 'diffusion' in filename:
            dfiles.append(filename)

    data = []
    for i in dfiles:

        # Extract temperature for file name convention
        temp = i.strip().split('_')[-1]
        temp = float(temp[:-1])

        df = pd.read_csv(i, sep=' ')
        df['temp'] = temp  # Add a temperature value

        data.append(df)

    # Merge the importated data
    df = pd.concat(data)

    fig, ax = pl.subplots()

    # Filter by all and by each element
    columns = [i for i in df if '_' not in i]
    columns = [i for i in columns if 'temp' not in i]

    # Plot the diffusion for each element
    for i in columns:

        ax.plot(df['temp'], df[i], marker='.', linestyle='none', label=i)

    ax.set_ylabel('Diffusion [*10^-4 cm^2 s^-1]')
    ax.set_xlabel('Temperature [K]')
    ax.grid()
    ax.legend(loc='lower right')
    fig.tight_layout()
    fig.savefig(path+'/images/diffusion/DvT')
    pl.close('all')

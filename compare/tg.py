'''
This script compares the average Tg from runs in a directory.
The folders must have the following naming convention:
    sizeatom

Example: 4000atom4676
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import pyplot as pl

import pandas as pd
import numpy as np

import argparse
import logging
import glob

# Command line arguments
parser = argparse.ArgumentParser()
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


def compareTg(directory):
    '''
    Compare the glass transition temperature between sizes in a directory.

    inputs:
            directory = the export directory of calculation data
    '''

    # Grab Tg for each run
    data = {}
    for filename in glob.iglob(directory+'/**/tg', recursive=True):
        try:
            with open(filename) as file:
                for line in file:
                    tg = line.strip().split(' ')
                    tg = float(tg[0])

            run = filename.split('/')[-4]
            data[run] = tg

        except Exception:
            pass

    sizes = []
    for key in data:
        sizes.append(int(key.split('atom')[0]))

    # Get Tg for each size
    sizes = set(sizes)
    sizedata = {i: [] for i in sizes}
    counts = {i: 0 for i in sizes}  # The number of samples for each size
    for size in sizes:
        for key, value in data.items():
            if str(size) in key:
                sizedata[size].append(value)
                counts[size] += 1

    # Determine averages and STD
    avgdata = {}
    stddata = {}
    for key, value in sizedata.items():
        avg = np.mean(value)
        std = np.std(value)

        avgdata[key] = avg
        stddata[key] = std

    # Crate data with following order: size, avg, std, counts
    df = {}
    for key, value in sizedata.items():
        df[key] = [key, avgdata[key], stddata[key], counts[key]]

    fig, ax = pl.subplots()
    for key, value in df.items():
        ax.errorbar(
                    value[0],
                    value[1],
                    value[2],
                    marker='.',
                    label='Samples: '+str(value[3])
                    )

    ax.set_xlabel('System Size [atoms]')
    ax.set_ylabel('Tg [K]')
    ax.grid()
    ax.legend(loc='lower right')
    fig.tight_layout()
    fig.savefig(directory+'/plotTg')
    pl.close('all')

    df = pd.DataFrame(df, index=['size', 'mean', 'STD', 'samples'])
    df = df.T
    df['size'] = df['size'].astype(int)
    df['samples'] = df['samples'].astype(int)

    df.to_csv(directory+'/Tg', sep=' ')

compareTg(args.o)

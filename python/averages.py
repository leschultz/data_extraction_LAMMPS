from matplotlib import pyplot as pl
from analysis import analize as an

import pandas as pd
import numpy as np
import setup
import os

pl.switch_backend('agg')  # Added for plotting in cluster

# Directories
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# Grab file names from the txt directory
names = os.listdir(data_directory+'txt/')

# Grab the run names
count = 0
for item in names:
    names[count] = item.split('.')[0]
    count += 1


def eim(msd, mean_msd):
    ''' Take the error in the mean.'''

    # Save the number of columns and rows
    rows, columns = msd.shape

    # Subtract each MSD at every time from the average and square it
    out = []
    for i in range(rows):
        value = np.subtract(msd[i], mean_msd)
        value **= 2
        out.append(value)

    # Get STD for each timepoint
    std_msd = (np.sum(out, axis=0)/rows)**0.5

    # Get error in the mean for each timepoint
    eim_msd = std_msd/(rows**0.5)

    # Return the error in the mean
    return eim_msd


def avg(*args, **kwargs):
    '''
    Do analysis for every run.
    '''

    series = args[0]

    print('Analyzing all '+series+' runs')

    # Grab names that match the series input
    newnames = []
    for item in names:
        if series in item and series[0] == item[0]:
            newnames.append(item)

    # Gather plots, vibration, and MSD data for each run
    msd = []
    data = {}
    for name in newnames:
        run = an(name, *args[1:], **kwargs)
        run.response()
        run.rdf()
        value_msd = run.msd()
        msd.append(value_msd[1])

        for key in value_msd[2]:
            if data.get(key) is None:
                data[key] = []
            else:
                data[key].append(value_msd[2][key])

    # Step data from last iteration on previous loop
    time = value_msd[0]

    print('Taking the mean data for ' + series)

    # Take the mean row by row for each atom for MSD
    msd = np.array(msd)
    mean_msd = np.mean(msd, axis=0)

    # Get error in the mean for each timepoint
    eim_msd = eim(msd, mean_msd)

    # Get the mean MSD for atom types and EIM
    data_mean = {}
    eim_data = {}
    for key in data:
        data[key] = np.array(data[key])
        data_mean[key] = np.mean(data[key], axis=0)
        eim_data[key] = eim(data[key], data_mean[key])
        pl.errorbar(
                    time,
                    data_mean[key],
                    eim_data[key],
                    errorevery=50,
                    label='Element Type: %i' % key
                    )

    # Plot the mean MSD
    pl.errorbar(time, mean_msd, eim_msd, errorevery=50, label='Total MSD')
    pl.xlabel('Time [ps]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend()
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'_avgMSD')
    pl.clf()

    # Return the steps with their corresponding msd mean
    return time, mean_msd, eim_msd, data_mean, eim_data

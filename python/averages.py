from matplotlib import pyplot as pl
from analysis import analize as an

import pandas as pd
import numpy as np
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


def avg(series, start, stop, frequency, step=None, interval=None):
    '''
    Do analysis for every run.
    '''

    print('Analyzing all '+series+' runs')

    # Grab names that match the series input
    newnames = []
    for item in names:
        if series in item and series[0] == item[0]:
            newnames.append(item)

    # Gather plots, vibration, and MSD data for each run
    msd = []
    for name in newnames:
        run = an(name, start, stop, frequency, step, interval)
        run.response()
        value_msd = run.msd()
        msd.append(value_msd[1])

        # If the RDF at a specified step is wanted
        if step is not None:
            run.rdf(step)
        else:
            run.rdf()

    # Step data from last iteration on previous loop
    step = value_msd[0]

    print('Taking the mean data for ' + series)

    # Take the mean row by row for each atom for MSD
    msd = np.array(msd)
    mean_msd = np.mean(msd, axis=0)

    # Truncate the axis by inputs
    i = int(start/frequency)
    f = int(stop/frequency)

    # Plot the mean MSD
    pl.plot(step[i:f+1], mean_msd[i:f+1])
    pl.xlabel('Step [-]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend([series])
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'_avgMSD')
    pl.clf()

    # Return the steps with their corresponding msd mean
    return step, mean_msd

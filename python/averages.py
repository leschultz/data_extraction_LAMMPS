from matplotlib import pyplot as pl
from analysis import analize as an

import pandas as pd
import numpy as np
import os

pl.switch_backend('agg')  # Added for plotting in cluster

# Directories
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'

# Change to txt directory
os.chdir(data_directory+'txt/')

# Grab file names from the txt directory
names = os.listdir()

# Grab the run names
count = 0
for item in names:
    names[count] = item.split('.')[0]
    count += 1


def avg(series, start, stop, step=None):
    '''
    Do analysis for every run.
    '''

    print('Analyzing all '+series+' runs')

    # Grab names that match the series input
    newnames = []
    for item in names:
        if series in item:
            newnames.append(item)

    # Gather plots, vibration, and MSD data for each run
    msd = []
    for name in newnames:
        run = an(name, start, stop)
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

    # Plot the mean MSD
    pl.plot(step, mean_msd)
    pl.xlabel('Step [-]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend([series])
    pl.grid(True)
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'[K]_avgMSD')
    pl.clf()

    # Return the steps with their corresponding msd mean
    return step, mean_msd

from matplotlib import pyplot as pl
from analysis import analize as an

import pandas as pd
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
    data_msd = {}
    data_vib = {}
    for name in newnames:
        run = an(name, start, stop)
        run.response()
        value_vib = run.vibration()
        value_msd = run.msd()
        data_vib[name+'vib'] = value_vib[1]
        data_msd[name+'msd'] = value_msd[1]

        # If the RDF at a specified step is wanted
        if step is not None:
            run.rdf(step)
        else:
            run.rdf()

    # Step data from last iteration on previous loop
    data_vib['Step'] = value_vib[0]
    data_msd['Step'] = value_msd[0]

    # Make a dataframe from MSD data
    df_msd = pd.DataFrame(data=data_msd)
    df_msd.set_index('Step', inplace=True)

    # Make a dataframe from vibration data
    df_vib = pd.DataFrame(data=data_vib)
    df_vib.set_index('Step', inplace=True)

    # Grab the names to be averaged
    temps = []
    for item in newnames:
        item = item.split('K')[0]
        temps.append(item)

    # Gather temperatures to be averaged
    runs = list(set(temps))

    print('Taking the mean data for ' + series)

    # Take the mean row by row for each atom for MSD
    meandf_msd = df_msd.mean(axis=1)

    # Take teh mean row by row for each atom for vibration
    meandf_vib = df_vib.mean(axis=1)

    # Plot the mean MSD
    pl.plot(data_msd['Step'], meandf_msd)
    pl.xlabel('Step [-]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend([series])
    pl.grid(True)
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'[K]_avgMSD')
    pl.clf()

    msd = meandf_msd.tolist()  # Average MSD

    # Plot the mean vibration
    pl.plot(data_vib['Step'], meandf_vib)
    pl.xlabel('Step [-]')
    pl.ylabel('Vibration Averaged [A^2]')
    pl.legend([series])
    pl.grid(True)
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'[K]_avgvibration')
    pl.clf()

    vibration = meandf_vib.tolist()  # Average MSD

    steps = data_vib['Step']  # Steps for Average MSD

    # Return the steps with their corresponding msd mean
    return steps, msd, vibration

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

    # Gather plots and MSD data for each run
    data = {}
    for name in newnames:
        run = an(name, start, stop)
        run.vibration()
        run.response()
        value = run.msd()
        data[name+'msd'] = value[1]

        if step is not None:
            run.rdf(step)

    # Step data
    data['Step'] = value[0]

    # Make a dataframe from data
    df = pd.DataFrame(data=data)
    df.set_index('Step', inplace=True)

    # Grab the names to be averaged
    temps = []
    for item in newnames:
        item = item.split('K')[0]
        temps.append(item)

    # Gather temperatures to be averaged
    runs = list(set(temps))

    meandf = df.mean(axis=1)

    pl.plot(data['Step'], meandf)
    pl.xlabel('Step [-]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend([series])
    pl.grid(True)
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'[K]_avgMSD')
    pl.clf()

    steps = data['Step']
    msd = meandf.tolist()  # Average MSD

    # Return the steps with their corresponding msd mean
    return steps, msd

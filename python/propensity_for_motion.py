from numpy import array
from numpy import mean

import pandas as pd
import pickle
import os


def run_average(thing, frame, length, run):
    '''
    Takes averages of runs. The number of runs for each temperature needs
    to be the same length.
    '''

    count = 0
    for i in range(0, length, run+1):
        thing.append(
                     mean(array(list(frame[i:(count+1)*(run+1)])), axis=0)
                     )
        count += 1

    return thing


def propensity(stop):
    '''
    Averages for each run type are taken here for calculate the propensity for
    motion. However, all runs averaged must contain the same number of runs
    because of how data is handled.
    '''

    # Get the current directory and saved data analysis directory
    first_directory = os.getcwd()
    data_directory = first_directory+'/../data/analysis/'

    # Change to data analysis directory
    os.chdir(data_directory)

    # Load data
    with open('data.pickle', 'rb') as handle:
        df = pickle.load(handle)

    # Remove warning from dataframe slice
    pd.options.mode.chained_assignment = None  # default='warn'

    # Truncate data to take averages
    count = 0
    for item in df['steps']:
        df['steps'][count] = df['steps'][count][:stop]
        df['dists'][count] = df['dists'][count][:stop]
        count += 1

    max_run = int(max(df['run']))  # The number of runs for each temperature
    run_length = len(df['run'])  # The length of data analyzed

    # Create averages
    dists = []
    temps = []
    steps = []
    dists = run_average(dists, df['dists'], run_length, max_run)
    temps = run_average(temps, df['temperature'], run_length, max_run)
    steps = run_average(steps, df['steps'], run_length, max_run)
    df = {
          'temperature': temps,
          'distances': dists,
          'steps': steps
          }

    df = pd.DataFrame(data=df)
    df = df[[
             'temperature',
             'steps',
             'distances'
             ]]

    df = df.sort_values(['temperature'])
    df = df.reset_index(drop=True)

    # Save dataframe
    with open('averages.pickle', 'wb') as handle:
        pickle.dump(df, handle)

   # Go back to starting directory after loading data
    os.chdir(first_directory)

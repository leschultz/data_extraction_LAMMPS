from matplotlib import pyplot as pl

import pandas as pd
import numpy as np
import pickle
import os


def dist(middle):
    '''
    This function find the distance between points accross a defined middle of
    data processed.
    '''

    # Get the current directory and saved data analysis directory
    first_directory = os.getcwd()
    data_directory = first_directory+'/../data/analysis/'

    # Change to data analysis directory
    os.chdir(data_directory)

    # Load data that contain averages of the runs
    with open('averages.pickle', 'rb') as handle:
        df = pickle.load(handle)

    # Take the difference between a later point and the point before
    displacement = []
    for run in df['dists']:
        diff = []
        for item in range(int(len(run)/2)):
            diff.append(abs(run[middle+item]-run[item]))

        displacement.append(diff)

    df = {
          'temps': df['temps'],
          'steps': df['steps'][:middle],
          'dists': displacement
          }

    df = pd.DataFrame(data=df)
    df = df[['temps', 'steps', 'dists']]
    df = df.sort_values(['temps'])
    df = df.reset_index(drop=True)

    # Save the order of runs with names
    os.chdir(data_directory)

    # Save dataframe
    with open('propensity.pickle', 'wb') as handle:
        pickle.dump(df, handle)

    # Go back to starting directory
    os.chdir(first_directory)

from matplotlib import pyplot as pl

import pandas as pd
import pickle
import os


def propensity():
    '''
    This function sums the distance traveled between each period of recorded
    time. This is differenct than absolue position because it approximates
    total translation.
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
    for item1 in df['dists']:
        diff = [0.0]  # Initial point set to zero
        count = 0
        for item2 in item1[1:]:
            diff.append(abs(item1[count+1]-item1[count]))
            count += 1
        displacement.append(diff)

    # Take the sum off the previous steps for time
    displacement_sum = []
    for item1 in displacement:
        disp = []
        count = 0
        for item2 in item1:
            disp.append(sum(item1[:count]))
            count += 1

        displacement_sum.append(disp)

    df = {
          'temps': df['temps'],
          'steps': df['steps'],
          'dists': displacement_sum
          }

    df = pd.DataFrame(data=df)
    df = df[[
             'temps',
             'steps',
             'dists'
             ]]
    df = df.sort_values(['temps'])
    df = df.reset_index(drop=True)

    # Save the order of runs with names
    os.chdir(data_directory)

    # Save dataframe
    with open('propensity.pickle', 'wb') as handle:
        pickle.dump(df, handle)

    # Go back to starting directory
    os.chdir(first_directory)

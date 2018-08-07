from numpy.polynomial.polynomial import polyfit
from numpy import arange

import pandas as pd
import pickle
import os


def fit(innitial, final):
    '''
    This function takes the line of best fit for the propensity for motion.
    The linear_stop input defines the number of datapoints to linearize.
    '''

    # Get directori+es
    first_directory = os.getcwd()  # Python scripts
    data_directory = first_directory+'/../data/analysis/'  # Export

    # Change directory to where data from analysis is stored
    os.chdir(data_directory)

    # Load average data
    with open('averages.pickle', 'rb') as handle:
        df = pickle.load(handle)

    # Take line of best fit for each average
    count = 0
    slope = []
    intercept = []
    for item in df['temps']:
        b, m = polyfit(
                       df['steps'][count][innitial:final],
                       df['dists'][count][innitial:final],
                       1
                       )
        slope.append(m)
        intercept.append(b)
        count += 1

    # Use the Einstein diffusion relationship to calculate diffusion
    diffusion = []
    temps = []
    count = 0
    for item in slope:
        diffusion.append(item/6.0)
        temps.append(df['temps'][count])
        count += 1

    # Create dataframe to export diffusion values
    df = {'temps': temps, 'diffusion': diffusion}
    df = pd.DataFrame(data=df)
    df = df[['temps', 'diffusion']]
    df = df.sort_values(['temps'])
    df = df.reset_index(drop=True)

    # Save the data as a csv
    df.to_csv('diffusion.csv', sep='\t', index=False)

    # Change back to original directory
    os.chdir(first_directory)

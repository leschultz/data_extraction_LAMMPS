from matplotlib import pyplot as pl

import pandas as pd
import pickle
import os

# Get the current directory and saved data analysis directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/analysis/'

# Change to data analysis directory
os.chdir(data_directory)

with open('data.pickle', 'rb') as file:
    df = pickle.load(file)

x = []
for item in df['steps']:
    x.append(item)

y = []
for item in df['dists']:
    y.append(item)

count = 0
for item in x:
    pl.plot(x[count], y[count], '.')
    count += 1

pl.xlabel('Step [-]')
pl.ylabel('Mean Squared Displacement [A^2]')
pl.legend(df['temperatures'])
pl.grid(True)
pl.savefig('propensity_for_motion_time.png')
pl.clf()

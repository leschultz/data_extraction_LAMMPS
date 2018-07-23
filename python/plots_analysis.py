import matplotlib.pyplot as pl
import pandas as pd
import cPickle
import os

# Get the current directory and saved data analysis directory
first_directory = os.getcwd()
data_directory = first_directory+'/../data/analysis/'

# Change to data analysis directory
os.chdir(data_directory)


data = pd.read_csv(
                   'data_for_each_run_mean.txt',
                   sep=' ',
                   header=None
                   )

data.columns = ([
                 'temperature',
                 'temperature_std',
                 'distance',
                 'distance_std'
                 ])

pl.plot(
        data['temperature'],
        data['distance'],
        'b.'
        )

pl.xlabel('Temperature [K]')
pl.ylabel('Propensity for Motion [A^2]')
pl.grid(True)
pl.savefig('propensity_for_motion.png')
pl.clf()

with open('time.txt', 'rb') as file:
    x = cPickle.load(file)

with open('dist.txt', 'rb') as file:
    y = cPickle.load(file)

for key in x:
    pl.plot(x[key]*0.001, y[key], '.')
    pl.xlabel('Time [fs]')
    pl.ylabel('Root mean squared displacement [<r^2>]')
    pl.legend(['1500 [K]'])
    pl.grid(True)
    pl.show()

from matplotlib import pyplot as pl

import pandas as pd
import pickle
import os


def plot(stop):
    '''
    The stop argument allows the user to define the end of the interval for
    plotting data.
    '''

    # Get the current directory and saved data analysis directory
    first_directory = os.getcwd()
    data_directory = first_directory+'/../data/analysis/'
    image_directory = first_directory+'/../images/motion/'

    # Change to data analysis directory
    os.chdir(data_directory)

    with open('data.pickle', 'rb') as handle:
        df = pickle.load(handle)

    # Open the data containing averages for each temperature run
    with open('averages.pickle', 'rb') as handle:
        df_avg = pickle.load(handle)

    # Change to image directory after loading data
    os.chdir(image_directory)

    print('Plotting all mean squared diplacements together')

    # Gather values to plot
    x = []
    for item in df['steps']:
        x.append(item)

    y = []
    for item in df['dists']:
        y.append(item)

    # Plot all displacement values together
    print('Plotting the mean squared displacement for all')
    count = 0
    temperature_run = []
    for item in x:
        pl.plot(x[count], y[count])
        temperature_run.append(str(df['temperatures'][count])+' [K]')
        count += 1

    pl.xlabel('Step [-]')
    pl.ylabel('Mean Squared Displacement [A^2]')
    pl.legend(temperature_run)
    pl.grid(True)
    pl.savefig('mean_squared_displacement_all.png')
    pl.clf()

    # Plot displacements for each run
    count = 0
    for item in x:
        print(
              'Plotting mean squared displacement for ' +
              str(df['input_temperature'][count]) +
              'K_' +
              str(df['run'][count])
              )

        pl.plot(df['steps'][count][:stop], df['dists'][count][:stop])
        pl.xlabel('Step [-]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.legend([str(df['temperatures'][count])+' [K]'])
        pl.grid(True)
        pl.savefig(
                   'mean_squared_displacement_' +
                   str(df['input_temperature'][count]) +
                   'K_' +
                   str(df['run'][count])
                   )
        pl.clf()
        count += 1

    # Plot the averages together
    print('Plotting the propensity for motion for all')
    count = 0
    for item in df_avg['steps']:
        pl.plot(df_avg['steps'][count], df_avg['distances'][count])
        count += 1

    pl.xlabel('Step [-]')
    pl.ylabel('Propensity for motion <r^2> [A^2]')
    pl.legend(df_avg['temperature'])
    pl.grid(True)
    pl.savefig('propensity_for_motion_all.png')
    pl.clf

    # Go back to starting directory
    os.chdir(first_directory)

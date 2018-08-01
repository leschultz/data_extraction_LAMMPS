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

    # Open the data containing overal travel distance
    with open('propensity.pickle', 'rb') as handle:
        df_sum = pickle.load(handle)

    # Change to image directory after loading data
    os.chdir(image_directory)

    print('Plotting all mean squared diplacements together')

    # Plot all displacement values together
    print('Plotting the mean squared displacement for all')
    count = 0
    temperature_run = []
    for item in df['steps']:
        pl.plot(df['steps'][count][:stop], df['dists'][count][:stop])
        temperature_run.append(str(df['temps'][count])+' [K]')
        count += 1

    pl.xlabel('Step [-]')
    pl.ylabel('Mean Squared Displacement [A^2]')
    pl.legend(temperature_run)
    pl.grid(True)
    pl.savefig('mean_squared_displacement_all.png')
    pl.clf()

    # Plot displacements for each run
    count = 0
    for item in df['steps']:
        print(
              'Plotting mean squared displacement for ' +
              str(df['input_temps'][count]) +
              'K_' +
              str(df['run'][count])
              )

        pl.plot(df['steps'][count][:stop], df['dists'][count][:stop])
        pl.xlabel('Step [-]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.legend([str(df['temps'][count])+' [K]'])
        pl.grid(True)
        pl.savefig(
                   'mean_squared_displacement_' +
                   str(df['input_temps'][count]) +
                   'K_' +
                   str(df['run'][count])
                   )
        pl.clf()
        count += 1

    # Plot the averages together
    print('Plotting the propensity for motion for all')
    count = 0
    temperature_run = []
    for item in df_avg['steps']:

        pl.plot(df_avg['steps'][count][:stop], df_avg['dists'][count][:stop])
        temperature_run.append(str(df_avg['temps'][count])+' [K]')
        count += 1

    pl.xlabel('Step [-]')
    pl.ylabel('Propensity for motion <r^2> [A^2]')
    pl.legend(temperature_run)
    pl.grid(True)
    pl.savefig('propensity_for_motion_all.png')
    pl.clf()

    # Plot the averages separately
    count = 0
    for item in df_avg['temps']:
        print(
              'Plotting the propensity for motion for ' +
              str(df_avg['temps'][count]) +
              ' [K]'
              )

        pl.plot(df_avg['steps'][count][:stop], df_avg['dists'][count][:stop])
        pl.xlabel('Step [-]')
        pl.ylabel('Propensity for motion <r^2> [A^2]')
        pl.legend([str(df_avg['temps'][count])+' [K]'])
        pl.grid(True)
        pl.savefig(
                   'propensity_for_motion_' +
                   str(df_avg['temps'][count]) +
                   '.png'
                   )
        pl.clf()
        count += 1

    # Plot the data for the displacements over time for all
    print('Plotting distance traversed for all averaged runs')
    count = 0
    temperature_run = []
    for item in df_sum['steps']:
        pl.plot(df_sum['steps'][count][:stop], df_sum['dists'][count][:stop])
        temperature_run.append(str(df_sum['temps'][count])+' [K]')
        count += 1

    pl.ylabel('Distances summed <r^2> [A^2]')
    pl.xlabel('Step [-]')
    pl.legend(temperature_run)
    pl.grid(True)
    pl.savefig('distance_sum.png')
    pl.clf()

    # Plot the data for the displacements over time for each temperature
    count = 0
    for item in df_sum['steps']:
        print(
              'Plotting distances summed for ' +
              str(df_sum['temps'][count]) +
              ' [K]'
              )

        pl.plot(df_sum['steps'][count][:stop], df_sum['dists'][count][:stop])
        pl.ylabel('Distances summed <r^2> [A^2]')
        pl.xlabel('Step [-]')
        pl.legend([str(df_sum['temps'][count])+' [K]'])
        pl.grid(True)
        pl.savefig(
                   'distance_sum' +
                   str(df_sum['temps'][count]) +
                   '.png'
                   )
        pl.clf()
        count += 1

    # Go back to starting directory
    os.chdir(first_directory)

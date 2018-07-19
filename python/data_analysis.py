import matplotlib.pyplot as pl
import pandas as pd
import os
import re

from scipy import mean
from numpy import std

first_directory = os.getcwd()
lammpstrj_directory = first_directory+'/../data/lammpstrj/'
data_export_directory = first_directory+'/../data/analysis/'

# The names of mean dislacements for each run
lammpstrj_file_names = os.listdir(lammpstrj_directory)

# The actual temperatures and standard deviation variable
temp_mean = []
temp_std = []
dist_mean = []
dist_std = []
temps = []

# Gather the temprature and run number
names = []
for item in lammpstrj_file_names:
    if item.endswith('rate.lammpstrj'):
        name = item
        name = ''.join(name.split())
        names.append(name[:-15])

# Gather the data and from files
for item1 in names:

    # For each argument value generate graphs
    data = pd.read_csv(
                       '../data/txt/'+str(item1)+'.txt',
                       comment='#',
                       sep=' ',
                       skiprows=1,
                       header=None
                       )

    # This is the orger of exported data
    data.columns = ([
                     'Step',
                     'Temperature [K]',
                     'Pressure [bar]',
                     'Volume [A^3]',
                     'Potential Energy [eV]',
                     'Kinetic Energy [eV]'
                     ])

    # Settling temp from file name
    temperature_settled = []
    separator = 'K'
    for character in item1:
        if character != separator:
            temperature_settled.append(character)
        else:
            break
    temperature_settled = int(''.join(temperature_settled))
    temps.append(temperature_settled)

    # Look for the moment equilibration temperature is met
    count = 0
    while (data['Temperature [K]'][count] <= temperature_settled):
        count += 1

    # Grab average temperature and standard deviation from data
    temp_mean.append(mean(data['Temperature [K]'][count:]))
    temp_std.append(std(data['Temperature [K]'][count:]))

    # Grab the number of items from a file
    number_of_atoms = pd.read_csv(
                                  '../data/lammpstrj/' +
                                  str(item1) +
                                  '_rate.lammpstrj',
                                  skiprows=3,
                                  nrows=1,
                                  header=None
                                  )

    number_of_atoms = number_of_atoms[0][0]

    # The order of imported data
    columns = ([
                'id',
                'type',
                'x',
                'y',
                'z',
                'junk'
                ])

    # Capture the first step when equilibration temperature is met
    first_step = count*(number_of_atoms+9)+9

    # Imported positions from when equlibration temperature is met
    data1 = pd.read_csv(
                        '../data/lammpstrj/'+str(item1)+'_rate.lammpstrj',
                        sep=' ',
                        skiprows=first_step,
                        nrows=number_of_atoms,
                        header=None
                        )

    data1.columns = columns

    # Capture last step of trajectory data
    last_step = (
                 data['Step'][len(data['Step'])-1] -
                 data['Step'][0])*(number_of_atoms+9)+9

    # Final positions of atoms
    data2 = pd.read_csv(
                        '../data/lammpstrj/'+str(item1)+'_rate.lammpstrj',
                        sep=' ',
                        skiprows=last_step,
                        nrows=number_of_atoms,
                        header=None
                        )

    data2.columns = columns

    # 3D translations
    delta_x = data2['x']-data1['x']
    delta_y = data2['y']-data1['y']
    delta_z = data2['z']-data1['z']

    # Grab the mean of the squared displacement
    distance_traveled = delta_x**2.0+delta_y**2.0+delta_z**2.0
    dist_mean.append(distance_traveled.mean())
    dist_std.append(std(distance_traveled))

# Creating dataframe from lists
frame = {
         'names': names,
         'temp_mean': temp_mean,
         'temp_std': temp_std,
         'dist_mean': dist_mean,
         'dist_std': dist_std
         }

dataframe = pd.DataFrame(data=frame)

dataframe = dataframe[[
                       'names',
                       'temp_mean',
                       'temp_std',
                       'dist_mean',
                       'dist_std'
                       ]]

result = dataframe.sort_values(['names'])
result = result.reset_index(drop=True)

# Save data in analysis folder
os.chdir(data_export_directory)
result.to_csv(r'data_for_each_run', header=None, index=None, sep=' ', mode='a')

# Count the number of runs for each temperature
run_separator = '_'
run_numbers = []
for item in names:
    run_numbers.append(int(item.split(run_separator,1)[1]))

# Match the termperatures with their averages
run_number_max = max(run_numbers)
temp_mean_average = []
temp_std_average = []
dist_mean_average = []
dist_std_average = []

count = 0
while count < run_number_max:
    temp_mean_average.append(
                             (result['temp_mean'][count*run_number_max:
                              (1+count)*run_number_max]).mean()
                             )
    temp_std_average.append(
                            (result['temp_std'][count*run_number_max:
                             (1+count)*run_number_max]).mean()
                            )
    dist_mean_average.append(
                             (result['dist_mean'][count*run_number_max:
                              (1+count)*run_number_max]).mean()
                             )
    dist_std_average.append(
                            (result['dist_std'][count*run_number_max:
                             (1+count)*run_number_max]).mean()
                            )

    count += 1

pl.errorbar(
            temp_mean_average,
            dist_mean_average,
            dist_std_average,
            temp_mean_average,
            'b.'
            )
pl.xlabel('Temperature [K]')
pl.ylabel('Propensity for Motion [A^2]')
pl.grid(True)
pl.savefig('propensity_for_motion.png')
pl.clf()

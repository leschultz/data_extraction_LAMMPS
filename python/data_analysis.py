import matplotlib.pyplot as pl
import pandas as pd
import os
import re

first_directory = os.getcwd()
lammpstrj_directory = first_directory+'/../data/lammpstrj/'

# The names of mean dislacements for each runi
lammpstrj_file_names = os.listdir(lammpstrj_directory)

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


    # Grab the number of items from a file
    number_of_atoms = pd.read_csv(
                                  '../data/lammpstrj/' +
                                  str(item1) +
                                  '_final.lammpstrj',
                                  skiprows=3,
                                  nrows=1,
                                  header=None
                                  )

    number_of_atoms = number_of_atoms[0][0]

    # Settling temp from file name
    temperature_settled = []
    separator = 'K'
    for character in item1:
        if character != separator:
            temperature_settled.append(character)
        else:
            break
    temperature_settled = int(''.join(temperature_settled))

    # Look for the moment equilibration temperature is met
    count = 0
    while (data['Temperature [K]'][count] <= temperature_settled):
        count += 1

    # The order of imported data
    columns = ([
                'id',
                'type',
                'x',
                'y',
                'z',
                'junk'
                ])

    # Imported positions from when equlibration temperature is met
    data1 = pd.read_csv(
                        '../data/lammpstrj/'+str(item1)+'_rate.lammpstrj',
                        comment='#',
                        sep=' ',
                        skiprows=9+(9+number_of_atoms)*count,
                        nrows=number_of_atoms,
                        header=None
                        )

    data1.columns = columns

    # Initial positions of atoms
    data2 = pd.read_csv(
                        '../data/lammpstrj/'+str(item1)+'_final.lammpstrj',
                        comment='#',
                        sep=' ',
                        skiprows=9,
                        header=None
                        )

    data2.columns = columns

    # 3D translations
    delta_x = data2['x']-data1['x']
    delta_y = data2['y']-data1['y']
    delta_z = data2['z']-data1['z']

    # Grab the mean of the squared displacement
    distance_traveled = (delta_x**2.0+delta_y**2.0+delta_z**2.0)**2.0
    distance_traveled_average = distance_traveled.mean()

    # Save average data on a file in a directory
    directory = os.getcwd()
    os.chdir(directory+'/../data/analysis/')
    filewrite = open('distance_traveled_average_'+str(item1), 'w+')
    filewrite.write(str(distance_traveled_average))
    os.chdir(directory)
    filewrite.close()

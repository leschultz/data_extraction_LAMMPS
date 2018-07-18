import matplotlib.pyplot as pl
import pandas as pd
import os

from scipy import mean

first_directory = os.getcwd()
lammpstrj_directory = first_directory+'/../data/lammpstrj/'

# The names of mean dislacements for each run
lammpstrj_file_names = os.listdir(lammpstrj_directory)

# Gather the temprature and run number
names = []
for item in lammpstrj_file_names:
    if item.endswith('rate.lammpstrj'):
        name = item
        name = ''.join(name.split())
        names.append(name[:-15])

# Grab the temperatures for each travel distance
temperatures = {}
for item1 in names:
    separator = 'K'
    for item2 in ''.join(item1.split()):
        temperatures.update({float(item1[0:item1.find(separator)]): []})

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

    # Look for the moment equilibration temperature is met
    count = 0
    while (data['Temperature [K]'][count] <= temperature_settled):
        count += 1

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
    distance_traveled_average = distance_traveled.mean()

    # Grab the temperatures for each travel distance
    temperatures[
                 float(item1[0:item1.find(separator)])
                 ].append(distance_traveled_average)

# Taking the averages of distances
data_means = {}
for key, value in temperatures.iteritems():
    data_means[key] = mean(value)

# Creating arrays for plotting
temp = []
dist = []
for key, value in data_means.iteritems():
    temp.append(key)
    dist.append(data_means[key])

pl.plot(temp, dist, '.b')
pl.xlabel('Temperature [K]')
pl.ylabel('Propensity for Motion [A^2]')
pl.grid(True)
pl.show()

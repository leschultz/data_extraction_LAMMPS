from numpy import array
from scipy import mean

import pandas as pd
import pickle
import os

# The order of imported data from lammpstrj files
columns = ([
            'id',
            'type',
            'x',
            'y',
            'z',
            'junk'
            ])

# Function for loading data from lammpstrj files
def load_lammpstrj(name, skip, length, columns):

    # Imported positions from when equlibration temperature is met
    return pd.read_csv(
                       '../data/lammpstrj/'+name+'_rate.lammpstrj',
                       sep=' ',
                       skiprows=skip,
                       nrows=length,
                       header=None,
                       names = columns
                       )

# Get directories
first_directory = os.getcwd()  # Python scripts
lammpstrj_directory = first_directory+'/../data/lammpstrj/'  # Trajectory
data_export_directory = first_directory+'/../data/analysis/'  # Export

# The names of mean dislacements for each run
lammpstrj_file_names = os.listdir(lammpstrj_directory)

# Gather the temprature and run number
names = []
for item in lammpstrj_file_names:
    names.append(item.split('_rate.lammpstrj')[0])

# Gather the run numbers
run_numbers = []
for item in names:
    run_numbers.append(item.split('K_')[1])

# Variable to append data in order
temp_mean = []
steps = []
dists = []
temps = []

# Gather the data and from files
for item in names:

    # For each argument value generate graphs
    data = pd.read_csv(
                       '../data/txt/'+item+'.txt',
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
    temperature_settled = int(item.split('K')[0])
    temps.append(temperature_settled)

    # Look for the moment equilibration temperature is met
    # Added some beggining time to avoid odd spikes
    count = 100
    while (data['Temperature [K]'][count] >= temperature_settled):
        count += 1

    while (data['Temperature [K]'][count] <= temperature_settled):
        count += 1

    count_cut = count

    # Get the average temperature after cutoff
    temp_mean.append(mean(data['Temperature [K]'][count_cut:]))

    # Grab the number of items from a file
    number_of_atoms = load_lammpstrj(item, 3, 1, None)
    number_of_atoms = number_of_atoms[0][0]

    # Capture the first step when equilibration temperature is met
    first_step = count_cut*(number_of_atoms+9)+9

    # Imported positions from when equlibration temperature is met
    data1 = load_lammpstrj(item, first_step, number_of_atoms, columns)

    # Capture the number of RECORDED steps until the final step
    recording_frequency = (data['Step'][1]-data['Step'][0])
    last_step = (data['Step'][len(data['Step'])-1])/recording_frequency

    count = count_cut
    dists_per_interval = []
    while count <= last_step:
        # Load data at increments from datum positon
        data2 = load_lammpstrj(
                               item,
                               count*(number_of_atoms+9)+9,
                               number_of_atoms,
                               columns
                               )

        # 3D translations
        delta_x = data2['x']-data1['x']
        delta_y = data2['y']-data1['y']
        delta_z = data2['z']-data1['z']

        # Grab the mean of the squared displacement (make key for each run)
        distance_traveled = (delta_x**2.0+delta_y**2.0+delta_z**2.0)**(1.0/2.0)
        dists_per_interval.append(mean(distance_traveled)**(1.0/2.0))
        count += 1

    steps.append(list(data['Step'][count_cut:]))
    dists.append(dists_per_interval)

# Arbitrary cutoff of data (can change in the future)
stop_criterion = 170

steps_cut = []
for item in steps:
    steps_cut.append(item[:stop_criterion])

dists_cut = []
for item in dists:
    dists_cut.append(item[:stop_criterion])

# Normalize steps
count = 0
for item in steps_cut:
    steps_cut[count] = array(steps_cut[count]) - steps_cut[count][0]
    count += 1

df = {
      'input_temperature': temps,
      'temperatures': temp_mean,
      'run' : run_numbers,
      'steps': steps_cut,
      'dists': dists_cut
      }

df = pd.DataFrame(data=df)
df = df[[
         'input_temperature',
         'run',
         'temperatures',
         'steps',
         'dists'
         ]]

df = df.sort_values(['temperatures', 'run'])
df = df.reset_index(drop=True)

# Save data
os.chdir(data_export_directory)
with open('data.pickle', 'wb') as handle:
    pickle.dump(df, handle)

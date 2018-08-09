from numpy import array
from scipy import mean

import pandas as pd
import pickle
import os


def load_lammpstrj(name, skip, length, columns):
    '''This function gathers position data from lammpstrj files'''

    # Imported positions from when equlibration temperature is met
    return pd.read_csv(
                       '../data/lammpstrj/'+name+'_rate.lammpstrj',
                       sep=' ',
                       skiprows=skip,
                       nrows=length,
                       header=None,
                       names=columns
                       )


def analyze(initial_skip):
    '''
    This function gathers the mean squared displacement for atoms with respect
    to time. The first argument allows skipping odd transient behavior when
    calculating settling temperature step. For instance, an input of 1000 will
    make the analysis skip to 1000*100 if the data aquisition rate is 100
    steps/aquisition.
    '''

    # The order of imported data from lammpstrj files
    columns = ([
                'id',
                'type',
                'x',
                'y',
                'z',
                'junk'
                ])

    # Get directories
    first_directory = os.getcwd()  # Python scripts
    lammpstrj_directory = first_directory+'/../data/lammpstrj/'  # Trajectory
    data_directory = first_directory+'/../data/analysis/'  # Export

    # List the names of files in the lammpstrj directory
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

        print('Processing '+item)

        # For each argument value generate graphs
        data = pd.read_csv(
                           '../data/txt/'+item+'.txt',
                           comment='#',
                           sep=' ',
                           skiprows=1,
                           header=None
                           )

        # This is the order of exported data
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

        # Get the average temperature after cutoff
        temp_mean.append(mean(data['Temperature [K]'][initial_skip:]))

        # Grab the number of items from a file
        number_of_atoms = load_lammpstrj(item, 3, 1, None)
        number_of_atoms = number_of_atoms[0][0]

        # Capture the first step when equilibration temperature is met
        first_step = initial_skip*(number_of_atoms+9)+9

        # Imported positions from when equlibration temperature is met
        data1 = load_lammpstrj(item, first_step, number_of_atoms, columns)

        # Capture the number of RECORDED steps until the final step
        recording_frequency = data['Step'][1]-data['Step'][0]
        last_step = (data['Step'][len(data['Step'])-1])/recording_frequency

        count = initial_skip
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

            # Grab the mean squared displacement (NOT root mean squared)
            distance_traveled = (
                                 delta_x**2.0 +
                                 delta_y**2.0 +
                                 delta_z**2.0
                                 )**(1.0/2.0)

            dists_per_interval.append(mean(distance_traveled**(2.0)))
            count += 1

        steps.append(list(data['Step'][initial_skip:]))
        dists.append(dists_per_interval)

    # Cutoff data at minimum sample length so that all runs are equal length
    count = 0
    lengths_of_steps = []
    for item in steps:
        lengths_of_steps.append(len(steps[count]))
        count += 1

    # Find the minimum list length that is used to truncate all data
    stop_criterion = min(lengths_of_steps)

    # Cut the data in steps to the minimum
    steps_cut = []
    for item in steps:
        steps_cut.append(item[:stop_criterion])

    # Cut the distance data to the minimum
    dists_cut = []
    for item in dists:
        dists_cut.append(item[:stop_criterion])

    # Normalize steps
    count = 0
    for item in steps_cut:
        steps_cut[count] = array(steps_cut[count]) - steps_cut[count][0]
        count += 1

    # Create a pandas dataframe containing data from the analysis
    df = {
          'input_temps': temps,
          'temps': temp_mean,
          'run': run_numbers,
          'steps': steps_cut,
          'dists': dists_cut
          }

    df = pd.DataFrame(data=df)
    df = df[[
             'input_temps',
             'run',
             'temps',
             'steps',
             'dists'
             ]]

    df = df.sort_values(['input_temps', 'run'])
    df = df.reset_index(drop=True)

    # Save the order of runs with names
    os.chdir(data_directory)

    # Save dataframe
    with open('data.pickle', 'wb') as handle:
        pickle.dump(df, handle)

    # Go back to starting directory
    os.chdir(first_directory)

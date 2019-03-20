import pandas as pd
import numpy as np
import os

datapath = './'

energyfile = 'tg_energy.txt'
volumefile = 'tg_volume.txt'


def dictcreator(dictionary, keys, files):
    '''
    Create a dictionary to hold data given a convention.

    inputs:
        dictionary = The name of the empty wanted dictionary
        keys = The keys for the dictionary
        files = The Tg files for each possible method

    outputs:
        dictionary = The name of the wanted dictionary with keys
    '''

    # Create the needed dictionaries
    if dictionary.get(keys[0]) is None:
        dictionary[keys[0]] = {}
    if dictionary[keys[0]].get(keys[1]) is None:
        dictionary[keys[0]][keys[1]] = {}
    if dictionary[keys[0]][keys[1]].get(keys[2]) is None:
        dictionary[keys[0]][keys[1]][keys[2]] = {}
    if dictionary[keys[0]][keys[1]][keys[2]].get(keys[3]) is None:
        dictionary[keys[0]][keys[1]][keys[2]][keys[3]] = {
                                                          files[0]: np.nan,
                                                          files[1]: np.nan,
                                                          }

    return dictionary


def fileload(dictionary, keys, datafile, path, filelist):
    '''
    Load the Tg data from a txt file.

    inputs:
        dictionary = The dictionary containing data
        keys = The relevant key list
        datafile = The name of the file containing Tg
        path = The path to datafile
        filelist = The list of available files

    outputs:
    '''

    # Load available data
    if datafile in filelist:
        tg = np.loadtxt(os.path.join(path, datafile))
        dictionary[keys[0]][keys[1]][keys[2]][keys[3]][datafile] = tg

    return dictionary


# Find all the paths available in a directory
paths = os.walk(datapath)

systems = {}  # Store data
locations = {}  # Store job location
for path in paths:

    # Skip the loop if the file tree does not follow convention
    try:
        names = path[0].split('/')[-4:]
        system, composition, hold, job = names

        if '-' not in system:
            continue

    except Exception:
        continue

    # Compensate for odd names from google drive
    system = system.split(' ')[0]
    composition = composition.split(' ')[0]
    hold = hold.split(' ')[0]
    job = job.split(' ')[0]
    names = [system, composition, hold, job]

    files = [energyfile, volumefile]
    dictcreator(systems, names, files)  # Create keys if not present
    dictcreator(locations, names, files)  # Create keys if not present

    locations[system][composition][hold][job] = path[0].split('job')[0]

    fileload(systems, names, energyfile, path[0], path[2])
    fileload(systems, names, volumefile, path[0], path[2])

# Build a dataframe for all collected Tg values
columns = [
           'System',
           'Composition [decimal]',
           'Steps [-]',
           'Job',
           'Tg from E-3kT Curve [K]',
           'Tg from Specific Volume Curve [K]',
           'Location of Jobs'
           ]

df = pd.DataFrame(columns=columns)

count = 0  # Use the count to append row by row
for system in systems:
    for composition in systems[system]:
        for hold in systems[system][composition]:
            for job in systems[system][composition][hold]:
                # Create a row to hold values
                row = [
                       system,
                       composition,
                       hold,
                       job,
                       np.nan,
                       np.nan,
                       locations[system][composition][hold][job]
                       ]

                for method in systems[system][composition][hold][job]:

                    # If the energy method has values, then replace elements
                    if method == energyfile:
                        row[4] = systems[system][composition][hold][job][method]

                    # If the volume method has values, then replace elements
                    if method == volumefile:
                        row[5] = systems[system][composition][hold][job][method]

                df.loc[count] = row  # Append a row to the dataframe
                count += 1

# Alphabetically sort the dataframe
df = df.sort_values(
                    by=[
                        'System',
                        'Composition [decimal]',
                        'Steps [-]',
                        'Job'
                        ]
                        )
df = df.reset_index(drop=True)  # Reset the index

df['Steps [-]'] = df['Steps [-]'].apply(pd.to_numeric)
df.to_html('Tg.html')  # Export as an HTML table
df.to_pickle('Tg.pkl')  # Export as a pickle file

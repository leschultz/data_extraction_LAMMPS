from matplotlib import pyplot as pl

import pandas as pd
import numpy as np
import os

path = '../tests'

energyfile = 'tg_energy.txt'
volumefile = 'tg_volume.txt'


def dictcreator(dictionary, keys):
    '''
    Create a dictionary to hold data given a convention.

    inputs:
        dictionary = The name of the empty wanted dictionary
        keys = The keys for the dictionary

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
        if dictionary[keys[0]][keys[1]][keys[2]].get(datafile) is None:
            dictionary[keys[0]][keys[1]][keys[2]][datafile] = []

        tg = np.loadtxt(os.path.join(path, datafile))
        dictionary[keys[0]][keys[1]][keys[2]][datafile].append(tg)

    return dictionary


# Find all the paths available in a directory
paths = os.walk(path)

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

    dictcreator(systems, names)  # Create keys if not present
    dictcreator(locations, names)  # Create keys if not present

    locations[system][composition][hold] = path[0]

    fileload(systems, names, energyfile, path[0], path[2])
    fileload(systems, names, volumefile, path[0], path[2])

# Build a dataframe with custom column names
columns = [
           'System',
           'Composition [decimal]',
           'Steps [-]',
           'Mean Tg from E-3kT Curve [K]',
           'STD Tg from E-3kdT Curve [K]',
           'Number of Mean Tg Values from E-3kT [-]',
           'Mean Tg from Specific Volume Curve [K]',
           'STD Tg from Specific Volume Curve [K]',
           'Number of Mean Tg Values from Specific Volume Curve [-]',
           'Location of Jobs'
           ]

# Create a dataframe with only the columns
df = pd.DataFrame(columns=columns)

count = 0  # Use the count to append row by row
for system in systems:
    for composition in systems[system]:
        for hold in systems[system][composition]:

            # Create a row to hold values
            row = [
                   system,
                   composition,
                   hold,
                   np.nan,
                   np.nan,
                   np.nan,
                   np.nan,
                   np.nan,
                   np.nan,
                   locations[system][composition][hold]
                   ]

            for method, tg in systems[system][composition][hold].items():

                # If the energy method has values, then replace elements
                if method == energyfile:
                    row[3] = np.mean(tg)
                    row[4] = np.std(tg)
                    row[5] = len(tg)

                # If the volume method has values, then replace elements
                if method == volumefile:
                    row[6] = np.mean(tg)
                    row[7] = np.std(tg)
                    row[8] = len(tg)

            df.loc[count] = row  # Append a row to the dataframe
            count += 1

df = df.sort_values(by='System')  # Alphabetically sort the dataframe
df = df.reset_index(drop=True)  # Reset the index
df.to_html('Tg.html')  # Export as an HTML table

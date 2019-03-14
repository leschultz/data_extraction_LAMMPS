from matplotlib import pyplot as pl

import pandas as pd
import numpy as np
import os

path = '/home/nerve/Desktop/tg/tests'

energyfile = 'tg_energy.txt'
volumefile = 'tg_volume.txt'

# Find all the paths available in a directory
paths = os.walk(path)

systems = {}
for path in paths:

    system, composition, hold, job = path[0].split('/')[-4:]

    # Skip the loop if the file tree does not follow convention
    if '-' not in system:
        continue

    # Create the needed dictionaries
    if systems.get(system) is None:
        systems[system] = {}
    if systems[system].get(composition) is None:
        systems[system][composition] = {}
    if systems[system][composition].get(hold) is None:
        systems[system][composition][hold] = {}

    # Load available data
    if energyfile in path[2]:
        if systems[system][composition][hold].get('energytg') is None:
            systems[system][composition][hold]['energytg'] = []

        energytg = np.loadtxt(os.path.join(path[0], energyfile))
        systems[system][composition][hold]['energytg'].append(energytg)


    if volumefile in path[2]:
        if systems[system][composition][hold].get('volumetg') is None:
            systems[system][composition][hold]['volumetg'] = []

        volumetg = np.loadtxt(os.path.join(path[0], volumefile))
        systems[system][composition][hold]['volumetg'].append(volumetg)

columns = [
           'System',
           'Composition [decimal]',
           'Steps [-]',
           'Mean Tg from E-3kT Curve [K]',
           'STD Tg from E-3kdT Curve [K]',
           'Number of Mean Tg Values from E-3kT [-]',
           'Mean Tg from Specific Volume Curve [K]',
           'STD Tg from Specific Volume Curve [K]',
           'Number of Mean Tg Values from Specific Volume Curve [-]'
           ]

df = pd.DataFrame(columns=columns)

count = 0
for system in systems:
    for composition in systems[system]:
        for hold in systems[system][composition]:
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
                   ]

            for method, tg in systems[system][composition][hold].items():

                if method == 'energytg':
                    row[3] = np.mean(tg)
                    row[4] = np.std(tg)
                    row[5] = len(tg)

                if method == 'volumetg':
                    row[6] = np.mean(tg)
                    row[7] = np.std(tg)
                    row[8] = len(tg)

            df.loc[count] = row
            count += 1

df = df.sort_values(by='System')
df = df.reset_index(drop=True)
df.to_html('Tg.html')

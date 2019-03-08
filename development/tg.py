from development.tempinfoparser import inputinfo
from development.kneefinder import *

from scipy.interpolate import UnivariateSpline as spline

from matplotlib import pyplot as pl
from io import BytesIO

import pandas as pd
import numpy as np

import tarfile
import math
import os

# The path to the google drive data
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/Ni-Zr/Zr0.00/1000/job1'
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/Zr-Cu/Cu0.00/1000/job1'
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/Pd-Si/Si0.00/1000/job1'
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/Al-Sm/Sm0.00/1000/job1'
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/La-Al/Al0.00/1000/job1'

# Look for all directories as generator object
paths = os.walk(path)

# Loop for each path
for item in paths:

    if 'job' in item[0]:

        # Were parsed data will be stored
        data = []

        # Create a name from the path
        name = item[0].split('/')
        name = name[-4:]
        name = os.path.join(*name)
        savepath = os.path.join(*['./', name])

        # Print status
        print(name)

        # Grab the output archive file that contains run system data
        filename = os.path.join(*[item[0], 'outputs.tar.gz'])
        inputfile = os.path.join(*[item[0], 'dep.in'])

        # Some of the parameters from the LAMMPS input file
        param = inputinfo(inputfile)
        hold1 = param['hold1']

        # Open the archive
        archive = tarfile.open(filename, 'r')

        # Iterate for each file in the archive
        for member in archive.getmembers():

            # Open the file containing system data
            if '.out' in  str(member):
                content = (archive.extractfile(member)).read()
                content = content.splitlines()

                # Parse information in file
                count = 0  # Counter for headers later
                for line in content:

                    # Bunch of parsing
                    line = line.decode('utf-8')
                    line = line.split(' ')
                    line = [i for i in line if '' != i]

                    if line:
                        if (line[0] == 'Step' and count == 0):
                            headers = line
                            count = 1

                        if ('Created' in line and 'atoms' in line):
                            natoms = int(line[1])

                        try:
                                line = [float(i) for i in line]
                                data.append(line)

                        except Exception:
                            pass

        # System data as a dataframe with removed repeated steps
        dfsystem = pd.DataFrame(data, columns=headers)
        dfsystem = dfsystem.drop_duplicates('Step')
        dfsystem = dfsystem.reset_index(drop=True)

        # Check if needed data is present
        columns = list(dfsystem.columns)
        needed = ['TotEng', 'Volume']
        for item in needed:
            if item not in columns:
                break

        # Create the path to work in
        if not os.path.exists(name):
            os.makedirs(name)
        savepath = os.path.join(*['./', name])

        # Parsed data exported from LAMMPS
        dfsystem = dfsystem.loc[dfsystem['Step'] >= hold1]  # Start of run
        dfenergy = dfsystem[['Temp', 'TotEng']]  # Energies and Temperature
        dfenergy.loc[:, 'TotEng'] = dfenergy['TotEng'].divide(natoms)
        dfenergy = dfenergy.sort_values(by=['Temp'])

        x = list(dfenergy['Temp'])
        y = list(dfenergy['TotEng'])

        # Subtract 3kT form the total energy
        y = [i-3.0*8.6173303*(10**-5)*j for i, j in zip(y, x)]

        # Find the polynomial coefficients for a fit
        yfit, ddyfit, kneeindex = knees(x, y)
        plotknee(x, y, yfit, ddyfit, kneeindex, 'energy')

        #  Save the Data from the data frame
        dfenergy.to_csv(
                        savepath+'/tg_energy.txt',
                        sep=' ',
                        index=False
                        )

        # Repeat the procedure using specific volume
        dfvolume = dfsystem[['Temp', 'Volume']]  # Energies and Temperature
        dfvolume.loc[:, 'Volume'] = dfvolume['Volume'].divide(natoms)
        dfvolume = dfvolume.sort_values(by=['Temp'])

        x = list(dfvolume['Temp'])
        y = list(dfvolume['Volume'])

        # Find the polynomial coefficients for a fit
        yfit, ddyfit, kneeindex = knees(x, y)
        plotknee(x, y, yfit, ddyfit, kneeindex, 'volume')

        # Save the Data from the data frame
        dfvolume.to_csv(
                        savepath+'/tg_volume.txt',
                        sep=' ',
                        index=False
                        )

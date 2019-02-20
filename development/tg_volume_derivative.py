from infoparser import inputinfo

from matplotlib import pyplot as pl
from io import BytesIO

import pandas as pd
import numpy as np

import tarfile
import math
import os

# The path to the google drive data
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/La-Al/Al1.00/667/job1'
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/Al-Ag/Ag1.00/667/job1'
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/La-Al/Al0.00/667/job1'

# Look for all directories as generator object
paths = os.walk(path)

# Define the percent of data for the fits
top = 50.0
bottom = 15.0

# Loop for each path
for item in paths:

    if 'job' in item[0]:

        # Were parsed data will be stored
        data = []

        # Create a name from the path
        name = item[0].split('/')
        name = name[-4:]
        name = os.path.join(*name)
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

        # Parsed data exported from LAMMPS
        dfsystem = dfsystem.loc[dfsystem['Step'] >= hold1]  # Start of run
        dfenergy = dfsystem[['Temp', 'Volume']]  # Energies and Temperature
        dfenergy.loc[:, 'Volume'] = dfenergy['Volume'].divide(natoms)
        dfenergy = dfenergy.sort_values(by=['Temp'])

        x = list(dfenergy['Temp'])
        y = list(dfenergy['Volume'])

        # Find the polynomial coefficients for a fit
        degree = 12
        coeffs = np.polyfit(x, y, degree)

        # Find the derivative of a polynomical
        dcoeffs = np.polyder(coeffs)
        ddcoeffs = np.polyder(dcoeffs)

        yfit = np.polyval(coeffs, x)
        dyfit = np.polyval(dcoeffs, x)
        ddyfit = np.polyval(ddcoeffs,x)

        # Find the peak of the second derivative
        count = 0
        for i, j in zip(ddyfit[:-1], ddyfit[1:]):
            # Break if the next value is less than
            if j < i:
                break

            count += 1

        print(x[count])

        fig, ax = pl.subplots()
        ax.plot(x, y, '.', label='Data')
        ax.plot(x, yfit, label='Polynomial Fit Degree '+str(degree))

        savepath = os.path.join(*['./', name])

        if not os.path.exists(name):
            os.makedirs(name)
        savepath = os.path.join(*['./', name])


        dfenergy.to_csv(
                        savepath+'/tg_energy.txt',
                        sep=' ',
                        index=False
                        )

        imagepath = savepath+'/tg_energy.png'

        ax.set_ylabel('Specific Volume [A^3/atom]')
        ax.grid()
        ax.legend(loc='upper right')
        plot = ax.get_figure()
        plot.tight_layout()
        plot.savefig(imagepath)

        ddax = ax.twinx()
        ddax.plot(x, ddyfit, label='Second Derivative of Fit', color='r')
        ddax.axvline(x[count], color='k', linestyle='--', label='Tg='+str(x[count])+' K')

        savepath = os.path.join(*['./', name])

        imagepath = savepath+'/tg_volume_derivative.png'

        ddax.set_xlabel('Temperature [K]')
        ddax.set_ylabel('[A^3/(atom*K^2])')
        ddax.grid()
        ddax.legend(loc='lower right')
        plot = ax.get_figure()
        plot.tight_layout()
        plot.savefig(imagepath)
        pl.close('all')

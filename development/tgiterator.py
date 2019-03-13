from development.tempinfoparser import inputinfo
from development.kneefinder import *

import pandas as pd
import numpy as np

import tarfile
import os


def findtg(path):
    '''
    Try to find the glass transition temperature based on energy and
    volume curves with respect to temperature.

    inputs:
        path = The path for the runs of interest

    outputs:
        Images and data files
    '''

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
                if '.out' in str(member):
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
            dfsystem = dfsystem.loc[dfsystem['Step'] >= hold1]  # Start of run
            dfsystem = dfsystem.sort_values(by=['Temp'])  # Needed for spline

            t = dfsystem['Temp'].values  # Temperatures

            # Attempt to do the energy analysis if data is available
            try:
                # Energies normalized by the number of atoms
                e = dfsystem['TotEng'].values/natoms
                tg(t, e, name, 'energy')
                print('Generated E-3kT vs. Temperature plot.')

            except Exception:
                pass

            # Attempt to do the volume analysis if data is available
            try:
                # Volumes normalized by the number of atoms
                v = dfsystem['Volume'].values/natoms
                tg(t, v, name, 'volume')
                print('Generated Specific Volume vs. Temperature plot.')

            except Exception:
                pass

    print('-'*79)


def tg(x, y, name, option):
    '''
    Determine the glass transition temperature with respect to temperature
    and energy or volume values. Data inserted must be strictly increasing.

    inputs:
        x = The temperature data
        y = The energy data
        name = The name of the run
        option = The analysis of energy or volume

    ouputs:
        Images and calculation values
    '''

    if option == 'energy':
        # Subtract 3kT form the total energy
        y = y-3.0*8.6173303*(10.0**-5.0)*x

    # Find the polynomial coefficients for a fit
    xfit, yfit, ddyfit, kneeindex = knees(x, y)

    # Create the path to work in
    if not os.path.exists(name):
        os.makedirs(name)
    savepath = os.path.join(*['./', name])

    plotknee(x, y, xfit, yfit, ddyfit, kneeindex, savepath+'/'+option)

    #  Save the Data from the data frame
    data = np.column_stack((x, y))
    np.savetxt(
               savepath+'/tg_'+option+'.txt',
               data,
               delimiter=' '
               )

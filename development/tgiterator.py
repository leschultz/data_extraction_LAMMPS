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
        finddata(item)


def finddata(item):
    '''
    Find the system data in compressed tar files for calculating the glass
    transition temperature.

    inputs:
        item = The path for where data may be

    outputs:
        A collection of images and data files for the glass transition
        temperature
    '''

    if 'job' in item[0]:

        # Create a name from the path
        name = item[0].split('/')
        name = name[-4:]
        name = os.path.join(*name)
        savepath = os.path.join(*['./', name])

        # Print status
        print('Tg analysis for: '+name)

        # Grab the output archive file that contains run system data
        systemfile = os.path.join(*[item[0], 'test.out'])
        inputfile = os.path.join(*[item[0], 'dep.in'])

        # Some of the parameters from the LAMMPS input file
        param = inputinfo(inputfile)
        hold1 = param['hold1']

        # Were parsed data will be stored
        data = []
        with open(systemfile) as content:

            # Parse information in file
            count = 0  # Counter for headers later
            for line in content:

                line = line.split(' ')
                line = [i for i in line if '' != i]

                if line:
                    if (line[0] == 'Step' and count == 0):
                        headers = line[:-1]
                        count = 1

                    if ('Created' in line and 'atoms\n' in line):
                        natoms = int(line[1])

                    try:
                        line = [float(i) for i in line[:-1]]
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
               savepath+'/tg_'+option+'_curve.txt',
               data,
               delimiter=' '
               )

    # Export the glass transition temperature
    with open(savepath+'/tg_'+option+'.txt', 'w+') as outfile:
        outfile.write(str(xfit[kneeindex]))

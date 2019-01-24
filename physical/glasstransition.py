'''
ICO cluster analysis for all steps in a run.
The trajectories at the end of each step is used.
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from scipy.interpolate import UnivariateSpline
from matplotlib import pyplot as pl
from scipy import stats as st

import pandas as pd
import numpy as np

import logging
import math

from setup.setup import exportdir as createfolders

from importers.outimport import *

# Format the logging style
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
                              '%(asctime)s - ' +
                              '%(name)s - ' +
                              '%(levelname)s - ' +
                              '%(message)s'
                              )
ch.setFormatter(formatter)


def run(param, exportdir, bottom, top):
    '''
    Iterate initial data analysis for all steps in all runs
    '''

    # Setup logger
    logger = logging.getLogger('Start')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.info('Tool Initialized')

    # Apply for each run in the main directory
    for item in param:

        path = item.replace('traj.lammpstrj', '')  # Run directory
        folder = '/'+path.split('/')[-2]  # Run name
        outfile = path+'test.out'  # LAMMPS data export
        createfolders(exportdir+folder)  # Create relevant folders

        # Setup logger
        logger = logging.getLogger('Tg Run: '+folder)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        printname = 'Gathering Data from File: '+item

        # Print on screen the run analyzed
        print('-'*len(printname))
        print(printname)
        print('-'*len(printname))

        # Parsed parameters
        n = param[item]['iterations']
        increment = param[item]['increment']
        deltatemp = param[item]['deltatemp']
        starttemp = param[item]['tempstart']
        timestep = param[item]['timestep']
        dumprate = param[item]['dumprate']
        hold1 = param[item]['hold1']
        hold2 = param[item]['hold2']
        hold3 = param[item]['hold3']
        trajsteps = param[item]['trajectorysteps']

        # The path to save in
        savepath = exportdir+'/'+item.split('/')[-2]

        # The number of atoms
        natoms = atoms(outfile)

        # Parsed data exported from LAMMPS
        dfsystem = readdata(outfile)  # System data
        dfsystem = dfsystem.loc[dfsystem['Step'] >= hold1]  # Start of run
        dfenergy = dfsystem[['Temp', 'TotEng']]  # Energies and Temperatures
        dfenergy.loc[:, 'TotEng'] = dfenergy['TotEng'].divide(natoms)

        xdata = list(dfenergy['Temp'])
        ydata = list(dfenergy['TotEng'])

        # Fit the higher temperature range
        length = len(xdata)
        start0 = 0
        end0 = math.floor((top/100)*length)

        x0 = xdata[start0:end0]
        y0 = ydata[start0:end0]
        fit0 = np.polyfit(x0, y0, 1)
        fitf0 = np.poly1d(fit0)
        yfit0 = fitf0(xdata)

        fitrange0 = str([math.floor(xdata[start0]), math.floor(xdata[end0])])

        # Fit the lower temperature range
        start1 = math.ceil((1-bottom/100)*length)
        end1 = -1
        x1 = xdata[start1:end1]
        y1 = ydata[start1:end1]

        fit1 = np.polyfit(x1, y1, 1)
        fitf1 = np.poly1d(fit1)
        yfit1 = fitf1(xdata)

        fitrange1 = str([math.floor(xdata[start1]), math.floor(xdata[end1])])

        try:
            npoints = 2
            point = [0]*(npoints+1)  # A point larger than 1 to start with
            tolerance = abs(max(ydata)-min(ydata))  # The initial tolerance

            # Iterate until point of intersection is found between fits
            count = 0
            while len(point) > npoints:
                condition = np.isclose(yfit0, yfit1, atol=tolerance)
                point = np.argwhere(condition).reshape(-1)
                tolerance -= tolerance/10

                if count > 100:
                    break

                count += 1

            temps = np.array(xdata)[point]
            temp = math.floor(sum(temps)/len(temps))
            sub.axvline(
                        x=temp,
                        linestyle='--',
                        label='Fit Intersection at '+str(temp)+' [K]'
                        )

        except Exception:
            pass

        dfenergy.to_csv(
                        savepath+'/datacalculated/tg/tg_energy.txt',
                        sep=' ',
                        index=False
                        )

        imagepath = savepath+'/images/tg/tg_energy.png'

        ax = dfenergy.plot(x='Temp', style='.')
        ax.plot(xdata, yfit0, 'r', label='Fit Range of '+fitrange0+' [K]')
        ax.plot(xdata, yfit1, 'g', label='Fit Range of '+fitrange1+' [K]')

        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Total Energy [eV/atom]')
        ax.grid()
        ax.legend(loc='best')
        plot = ax.get_figure()
        plot.tight_layout()
        plot.savefig(imagepath)
        pl.close('all')

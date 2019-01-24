'''
ICO cluster analysis for all steps in a run.
The trajectories at the end of each step is used.
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import pyplot as pl
from scipy import stats as st

import pandas as pd
import numpy as np

import logging

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


def run(param, exportdir):
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

        # Setup logger
        logger = logging.getLogger('Tg Run: '+folder)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        dfenergy.to_csv(
                        savepath+'/datacalculated/tg/tg_energy.txt',
                        sep=' ',
                        index=False
                        )

        imagepath = savepath+'/images/tg/tg_energy.png'

        ax = dfenergy.plot(x='Temp', style='.')
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Total Energy [eV/atom]')
        ax.grid()
        plot = ax.get_figure()
        plot.tight_layout()
        plot.savefig(imagepath)
        pl.close('all')

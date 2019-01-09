'''
Calculate the diffusion and RDF data from a set of data.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
from matplotlib import pyplot as pl
from physical.ovito_calc import calc, rdfcalc
from scipy.stats import linregress
from setup.setup import exportdir

import pandas as pd
import numpy as np


def diffusion(time, msd):
    '''
    Calculate the diffusivity from a linear fit of MSD data.

    inputs:
            time = the time data set
            msd = the mean squared displacement dataset
    outputs:
            diffusion = diffusion by the Einstein relationship
    '''

    # Calculate the self diffusion coefficient [*10^-4 cm^2 s^-1]
    diffusion = {}
    for key in msd:
        if '_EIM' not in key:
            p = linregress(time, msd[key])
            slope = p[0]
            stderr = p[-1]
            diffusion[key] = slope/6.0
            diffusion[key+'_err'] = stderr/6.0

    return diffusion


class analize(object):
    '''A class to add freedon on what data is calculated'''

    def __init__(
                 self,
                 run,
                 savepath,
                 start,
                 stop,
                 timestep,
                 dumprate,
                 step=None,
                 cut=10,
                 bins=50
                 ):

        '''Load data and set variables used throughout methods'''

        # Create the folder for where data will be saved
        exportdir(savepath)
        self.savepath = savepath

        # The name of the run
        self.run = run.split('.')[0]
        self.run = self.run.split('/')[-1]

        # Relevant file (trajectories)
        self.trjfile = run

        self.timestep = timestep  # The step size used in LAMMPS

        # The rate of data acquisition and number of atoms
        self.frq = dumprate

        self.bins = bins  # The number of bins
        self.cut = cut  # Data for RDF
        self.step = step  # The step to plot RDF

        # Inclusive start and stop conditions
        self.start = start  # Start Step
        self.stop = stop  # Stop step

        # The start and stopping frames
        self.startframe = int(self.start/self.frq)
        self.stopframe = int(self.stop/self.frq)

        # Where all relevant data is stored
        self.data = {}

    def calculate_time(self):
        '''
        Calculate the time from the steps.
        '''

        self.steps = list(range(0, self.stop-self.start+1, self.frq))
        time = [i*self.timestep for i in self.steps]  # Time from steps
        self.time = [i-time[0] for i in time]  # Normalize time

    def calculate_msd(self):
        '''
        Gather data for MSD.
        '''

        # Gather the MSD values
        self.msd = calc(
                        self.trjfile,
                        self.startframe,
                        self.stopframe
                        )

        self.msd = pd.DataFrame(self.msd)

    def calculate_rdf(self):
        '''
        Gather the RDF dat from Ovito.
        '''

        headers = ['r', 'gr']

        # Gather the RDF for steps defined
        if self.step is not None:
            self.rdf = {}
            for item in self.step:
                if self.rdf.get(item) is None:
                    self.rdf[item] = []

                self.rdf[item] = rdfcalc(
                                         self.trjfile,
                                         int(item/self.frq),
                                         self.cut,
                                         self.bins
                                         )

                self.rdf[item] = pd.DataFrame(self.rdf[item], columns=headers)

    def calculate_diffusion(self):
        '''
        Calculate the diffusivity from a linear fit of MSD data.
        '''

        # Calculate the self diffusion coefficient [*10^-4 cm^2 s^-1]
        self.diffusion = diffusion(self.time, self.msd)

    def multiple_origins_diffusion(self):
        '''
        Calculate the diffusion by multiple origins method.
        '''

        # The number of relevant frames
        length = self.stopframe-self.startframe

        # Split the relevant region
        N = 2
        halflength = length//N

        # The time in the relevant frames
        time = self.time[0:halflength+1]

        diffmulti = {}
        for key in self.diffusion:
            diffmulti[key] = []

        self.mostart = []
        self.mostop = []
        count = 0
        while count <= halflength:

            start = self.startframe+count
            stop = self.startframe+count+halflength

            # Gather the MSD values
            msd = calc(
                       self.trjfile,
                       start,
                       stop
                       )

            # Calculate the diffusion from each line of MSD
            diff = diffusion(time, msd)

            # Save the time range for each line of best fit
            self.mostart.append(count*self.frq*self.timestep)
            self.mostop.append((halflength+count)*self.frq*self.timestep)

            # Save the diffusion for each line of bet fit
            for key in diff:
                diffmulti[key].append(diff[key])

            count += 1

        self.diffmulti = pd.DataFrame(diffmulti)

    def calculation_export(self):
        '''
        Return the data for calculated properties.
        '''

        return self

    def save_msd(self, savename):
        '''
        Method for saving MSD data

        inputs:
                savename = the name of the data file
        '''

        export = self.savepath+'/datacalculated/msd/'+savename

        df = self.msd.copy()
        df.insert(0, 'time', self.time)
        df.to_csv(export, sep=' ', index=False)

    def save_multiple_origins_diffusion(self, savename):
        '''
        Save the diffusion data for multiple origins

        inputs:
                savename = the name of the data file
        '''

        output = (
                  self.savepath +
                  '/datacalculated/diffusion/' +
                  savename +
                  '_MO'
                  )

        df = self.diffmulti.copy()
        df.insert(0, 'start_time', self.mostart)
        df.insert(1, 'stop_time', self.mostop)
        df.to_csv(output, sep=' ', index=False)

    def save_rdf(self, savename):
        '''
        Method for saving the RDF data

        inputs:
                savename = the name of the data file
        '''

        if self.step is not None:

            for key in self.rdf:
                df = pd.DataFrame(data=self.rdf[key])

                export = (
                          self.savepath +
                          '/datacalculated/rdf/' +
                          savename +
                          '_step_' +
                          str(key)
                          )

                df.to_csv(export, sep=' ', index=False)

    def save_diffusion(self, savename):
        '''
        Method for saving the diffusion data

        inputs:
                savename = the name of the data file
        '''

        export = (
                  self.savepath +
                  '/datacalculated/diffusion/' +
                  savename
                  )

        df = pd.DataFrame(data=self.diffusion, index=[0])
        df.to_csv(export, sep=' ', index=False)

    def plot_msd(self, savename):
        '''
        Plot mean squared displacement

        inputs:
                savename = the name of the image file
        '''

        # Control the frequency of errorbars
        errorfreq = len(self.time)//10
        if errorfreq == 0:
            errorfreq = 1

        for key in self.msd:
            if '_EIM' not in key:
                pl.errorbar(
                            self.time,
                            self.msd[key],
                            self.msd[key+'_EIM'],
                            label='Element Type: %s' % key,
                            errorevery=errorfreq
                            )

        pl.xlabel('Time [ps]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.legend(loc='upper left')
        pl.savefig(self.savepath+'/images/msd/'+savename)
        pl.clf()

    def plot_diffusion(self, savename):
        '''
        Plot the multiple origins diffusion

        inputs:
                savename = the name of the image file
        '''

        for key in self.diffmulti:
            if '_err' not in key:
                pl.errorbar(
                            self.mostart,
                            self.diffmulti[key],
                            self.diffmulti[key+'_err'],
                            label='element Type: %s' % key,
                            marker='.'
                            )

        pl.xlabel('Start Time [ps]')
        pl.ylabel('Diffusion [*10^-4 cm^2 s^-1]')
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.legend(loc='best')
        pl.savefig(self.savepath+'/images/diffusion/'+savename+'_MO')
        pl.clf()

    def plot_rdf(self, savename):
        '''
        Plot the radial distribution at a point and throughout time

        inputs:
                savename = the name of the image file
        '''

        # Plot the RDF for a specific timestep
        if self.step is not None:

            # Plot for every step in user input list
            for key in self.rdf:
                pl.plot(self.rdf[key]['r'], self.rdf[key]['gr'])
                pl.legend(['Step '+str(key)], loc='best')
                pl.xlabel('Bin Center [A]')
                pl.ylabel('g(r)')
                pl.grid(b=True, which='both')
                pl.tight_layout()
                pl.savefig(
                           self.savepath +
                           '/images/rdf/' +
                           savename +
                           '_step_' +
                           str(key) +
                           '_rdf'
                           )
                pl.clf()

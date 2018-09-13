from PyQt5 import QtGui  # Added to be able to import ovito
from matplotlib import pyplot as pl
from ovito_calc import calc, rdfcalc
from scipy.stats import linregress

import parameters as par
import pandas as pd
import numpy as np
import setup


class analize(object):
    '''Computation functions are defined here'''

    def __init__(
                 self,
                 run,
                 start,
                 stop,
                 stepsize,
                 dumprate,
                 step=None,
                 cut=10,
                 bins=50
                 ):

        '''Load data'''

        self.run = run  # The name of the run

        # Relevant files (trajectories and other LAMMPS outputs)
        self.trjfile = '../data/lammpstrj/'+self.run+'.lammpstrj'
        self.sysfile = '../data/txt/'+self.run+'.txt'

        self.stepsize = stepsize  # The step size used in LAMMPS

        # The rate of data acqusition and number of atoms
        param = par.gather(self.trjfile)
        self.size = param['size']
        self.frq = dumprate

        print('_'*79)
        print('Crunching data for: ')
        print(self.run)

        self.bins = bins  # The number of bins
        self.cut = cut  # Data for RDF
        self.step = step  # The step to plot RDF

        # Inclusive start and stop conditions
        self.start = start  # Start Step
        self.stop = stop  # Stop step

        # The start and stopping frames
        self.startframe = int(self.start/self.frq)
        self.stopframe = int(self.stop/self.frq)

    def calculate(self):
        '''
        Gather data for steps, MSD, RDF, and common neighborhood analysis.
        '''

        # All data to be returned
        data = {}

        # Gather the MSD and common neighbor values
        self.steps, self.msd = calc(
                                    self.trjfile,
                                    self.startframe,
                                    self.stopframe
                                    )

        # Gather the RDF for steps defined
        if self.step is not None:
            self.rdf = {}
            for item in self.step:
                if self.rdf.get(item) is None:
                    self.rdf[item] = []

                self.rdf[item] = (rdfcalc(
                                          self.trjfile,
                                          int(item/self.frq),
                                          self.cut,
                                          self.bins
                                          ))

            # The RDF data if the acquisition steps are defined
            data['rdf'] = self.rdf

        time = [i*self.stepsize for i in self.steps]  # Time from steps
        self.time = [i-time[0] for i in time]  # Normalize time

        # Calculate the self diffusion coefficient [*10^-4 cm^2 s^-1]
        self.diffusion = {}
        for key in self.msd:
            if '_EIM' not in key:
                p = linregress(self.time, self.msd[key])
                slope = p[0]
                stderr = p[-1]
                self.diffusion[key] = slope/6
                self.diffusion[key+'_Err'] = stderr/6

        data['time'] = self.time
        data['msd'] = self.msd
        data['diffusion'] = self.diffusion
        self.data = data

        return self.data

    def msdsave(self):
        '''
        Method for saving MSD data
        '''

        df = pd.DataFrame(data=self.data['msd'])
        df.insert(loc=0, value=self.data['time'], column='time')

        export = '../datacalculated/msd/'+self.run
        df.to_csv(export, index=False)

    def rdfsave(self):
        '''
        Method for saving the RDF data
        '''

        data = {}
        for key in self.data['rdf']:
            data['step_'+str(key)+'_coord'] = self.data['rdf'][key][0]
            data['step_'+str(key)+'_rdf'] = self.data['rdf'][key][1]

        df = pd.DataFrame(data=data)

        export = '../datacalculated/rdf/'+self.run
        df.to_csv(export, index=False)

    def diffusionsave(self):
        '''
        Method for saving the diffusion data
        '''

        df = pd.DataFrame(data=self.data['diffusion'], index=[0])

        export = '../datacalculated/diffusion/'+self.run
        df.to_csv(export, index=False)

    def plotmsd(self):
        '''
        Plot mean squared displacement.
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
        pl.savefig('../images/msd/'+self.run+'_MSD')
        pl.clf()

    def plotrdf(self):
        '''
        Plot the radial distribution at a point and throughout time.
        '''

        # Plot the RDF for a specific timestep
        if self.step is not None:

            # Plot for every step in user input list
            for key in self.rdf:
                pl.plot(self.rdf[key][0], self.rdf[key][1])
                pl.legend(['Step '+str(key)], loc='best')
                pl.xlabel('Bin Center [A]')
                pl.ylabel('g(r)')
                pl.grid(b=True, which='both')
                pl.tight_layout()
                pl.savefig(
                           '../images/rdf/' +
                           self.run +
                           '_step' +
                           str(key) +
                           '_rdf'
                           )
                pl.clf()

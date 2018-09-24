from PyQt5 import QtGui  # Added to be able to import ovito
from matplotlib import pyplot as pl
from ovito_calc import calc, rdfcalc
from scipy.stats import linregress

import parameters as par
import pandas as pd
import numpy as np
import setup


def diffusion(time, msd):
    '''
    Calculate the diffusivity from a linear fit of MSD data.
    '''

    # Calculate the self diffusion coefficient [*10^-4 cm^2 s^-1]
    diffusion = {}
    for key in msd:
        if '_EIM' not in key:
            p = linregress(time, msd[key])
            slope = p[0]
            stderr = p[-1]
            diffusion[key] = slope/6
            diffusion[key+'_Err'] = stderr/6

    return diffusion


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

        # Where all relevant data is stored
        self.data = {}

    def calculate_time(self):
        '''
        Calculate the time from the steps.
        '''

        self.steps = list(range(0, self.stop-self.start+1, self.frq))
        time = [i*self.stepsize for i in self.steps]  # Time from steps
        self.time = [i-time[0] for i in time]  # Normalize time
        self.data['time'] = self.time

    def calculate_msd(self):
        '''
        Gather data for MSD.
        '''

        # Gather the MSD values
        self.steps, self.msd = calc(
                                    self.trjfile,
                                    self.startframe,
                                    self.stopframe
                                    )

        self.data['msd'] = self.msd

    def calculate_rdf(self):

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
            self.data['rdf'] = self.rdf

    def calculate_diffusion(self):
        '''
        Calculate the diffusivity from a linear fit of MSD data.
        '''

        # Calculate the self diffusion coefficient [*10^-4 cm^2 s^-1]
        self.diffusion = diffusion(self.time, self.msd)
        self.data['diffusion'] = self.diffusion

    def multiple_origins_diffusion(self):
        '''
        Calculate the diffusion by multiple origins method.
        '''

        # The number of relevant frames
        length = self.stopframe-self.startframe

        # The time in the relevant frames
        time = self.time[0:length]

        # Split the relevant region in half
        N = 2
        halflength = length//N

        # Iterate for multiple origins
        count = 0
        diffmulti = {}

        for key in self.diffusion:
            diffmulti[key] = []

        while count <= halflength:

            # Gather the MSD values
            steps, msd = calc(
                              self.trjfile,
                              self.startframe+count,
                              self.stopframe+count-halflength
                              )

            diff = diffusion(time, msd)

            for key in diff:
                diffmulti[key].append(diff[key])

            count += self.frq

        self.diffmulti = diffmulti
        self.data['diffusion_multiple_origins'] = self.diffmulti

    def calculation_export(self):
        '''
        Return the data for calculated properties.
        '''

        return self.data

    def save_msd(self):
        '''
        Method for saving MSD data
        '''

        df = pd.DataFrame(data=self.data['msd'])
        df.insert(loc=0, value=self.data['time'], column='time')

        export = '../datacalculated/msd/'+self.run
        df.to_csv(export, index=False)

    def save_diffusion_multiple_origins(self):
        '''
        Save the diffusion data for multiple origins.
        '''

        fmt = ''
        nh = ''
        for key in self.diffmulti:
            fmt += '%f '
            nh += key+' '

        output = '../datacalculated/diffusion/'+item+'_origins'

        df = pd.DataFrame(data=diffmulti)
        df.insert(0, 'time', startpoints)
        df.to_csv(output, sep=' ', index=False)

    def save_rdf(self):
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

    def save_diffusion(self):
        '''
        Method for saving the diffusion data
        '''

        df = pd.DataFrame(data=self.data['diffusion'], index=[0])

        export = '../datacalculated/diffusion/'+self.run
        df.to_csv(export, index=False)

    def plot_msd(self):
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

    def plot_rdf(self):
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

from PyQt5 import QtGui  # Added to be able to import ovito
from matplotlib import pyplot as pl
from ovito_calc import calc, rdfcalc

import parameters as par
import subprocess as sub
import tempfile as temp
import pandas as pd
import numpy as np
import shlex
import os

# Get relevant directories
first_directory = os.getcwd()
data_directory = first_directory + '/../data/analysis/'
msd_directory = data_directory + 'msd/'
rdf_directory = data_directory + 'rdf/'
clu_directory = data_directory + 'cluster/'


class analize(object):
    '''Computation functions are defined here'''

    def __init__(
                 self,
                 run,
                 start,
                 stop,
                 stepsize,
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
        self.frq = param['rate']
        self.size = param['size']

        print('Crunching data for '+self.run)

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
        self.steps, self.msd, self.clu = calc(
                                              self.trjfile,
                                              self.startframe,
                                              self.stopframe
                                              )

        # Gather the RDF for steps defined
        if self.step is not None:
            self.rdf = []
            for item in self.step:
                self.rdf.append(rdfcalc(
                                        self.trjfile,
                                        int(item/self.frq),
                                        self.cut,
                                        self.bins
                                        ))

            # The RDF data if the acquisition steps are defined
            data['rdf'] = self.rdf

        time = [i*self.stepsize for i in self.steps]  # Time from steps
        self.time = [i-time[0] for i in time]  # Normalize time

        # Average the count of clusters over time
        self.fccavg = np.sum(self.clu['fcc'])/self.time[-1]
        self.hcpavg = np.sum(self.clu['hcp'])/self.time[-1]
        self.bccavg = np.sum(self.clu['bcc'])/self.time[-1]
        self.icoavg = np.sum(self.clu['ico'])/self.time[-1]

        # Normalize cluster count by system size
        self.fccavg = self.fccavg/self.size
        self.hcpavg = self.hcpavg/self.size
        self.bccavg = self.bccavg/self.size
        self.icoavg = self.icoavg/self.size

        data['time'] = self.time
        data['msd'] = self.msd
        data['fccavg'] = self.fccavg
        data['hcpavg'] = self.hcpavg
        data['bccavg'] = self.bccavg
        data['icoavg'] = self.icoavg

        return data

    def plotmsd(self):
        '''
        Plot mean squared displacement.
        '''

        for key in self.msd:
            pl.plot(
                    self.time,
                    self.msd[key],
                    label='Element Type: %s' % key
                    )

        pl.xlabel('Time [ps]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.legend(loc='upper left')
        pl.savefig('../images/motion/'+self.run+'_MSD')
        pl.clf()

    def plotclusters(self):
        '''
        Plot the common neighbor analysis.
        '''

        clusters = [self.fccavg, self.hcpavg, self.bccavg, self.icoavg]

        # The labels for clusters in the xlabel
        labels = ['FCC', 'HCP', 'BCC', 'ICO']
        location = [1, 2, 3, 4]

        count = 0
        for v, i in enumerate(clusters):
            pl.text(
                    v+1, i,
                    ' '+str(clusters[count]),
                    color='red',
                    ha='center',
                    fontweight='bold'
                    )

            count += 1

        pl.bar(location, clusters,  align='center')
        pl.xticks(location, labels)
        pl.xlabel('Cluster [-]')
        pl.ylabel('[count/(ps*size)]')
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.savefig('../images/cluster/'+self.run+'_cluster')
        pl.clf()

    def plotrdf(self):
        '''
        Plot the radial distribution at a point and throughout time.
        '''

        # Plot the RDF for a specific timestep
        if self.step is not None:

            # Plot for every step in user input list
            count = 0
            for item in self.step:
                pl.plot(self.rdf[count][0], self.rdf[count][1])
                pl.legend(['Step '+str(item)], loc='best')
                pl.xlabel('Bin Center [A]')
                pl.ylabel('g(r)')
                pl.grid(b=True, which='both')
                pl.tight_layout()
                pl.savefig('../images/rdf/'+self.run+'_'+str(item)+'_rdf')
                pl.clf()

                count += 1

    def plotresponse(self):
        '''
        Load the system properties throughout time.
        '''

        # Load the data
        mycolumns = [
                     'Step [-]',
                     'Temperature [K]',
                     'Pressure [bar]',
                     'Volumne [A^3]',
                     'Potential Energy [eV]',
                     'Kinetic Energy [eV]'
                     ]

        data = pd.read_csv(
                           self.sysfile,
                           names=mycolumns,
                           sep=' ',
                           comment='#',
                           header=None
                           )

        # Define time based on input stepsize
        time = [i for i in data['Step [-]']*self.stepsize]

        # Plot recorded data versus step
        for item in mycolumns:
            pl.plot(time, data[item])
            pl.xlabel('Time [ps]')
            pl.ylabel(item)
            pl.grid(b=True, which='both')
            pl.tight_layout()
            pl.savefig(
                       '../images/system/' +
                       self.run +
                       '_' +
                       item.split(' ')[0]
                       )
            pl.clf()

from matplotlib import pyplot as pl

import subprocess as sub
import tempfile as temp
import pandas as pd
import numpy as np
import shlex
import os

pl.switch_backend('agg')  # Added for plotting in cluster

# Get relevant directories
first_directory = os.getcwd()
data_directory = first_directory + '/../data/analysis/'
msd_directory = data_directory + 'msd'
rdf_directory = data_directory + 'rdf/'


class analize(object):
    '''Computation functions are defined here'''

    def __init__(
                 self,
                 name,
                 start,
                 stop,
                 frequency,
                 step=None,
                 cut=None,
                 bins=100
                 ):

        '''Load data'''

        self.run = name  # The name of the run
        self.frq = frequency  # The rate of data acquisition

        print('Crunching data for ' + self.run)

        self.bins = bins  # The number of bins
        self.cut = cut  # Data for RDF
        self.step = step  # The step to plot RDF

        # Inclusive start and stop conditions
        self.start = start  # Start Step
        self.stop = stop  # Stop step

    def msd(self):
        '''
        Calcualte the means squared displacement.
        '''

        ovitostring = (
                       "'import ovito_msd as ov; ov.msdcalc(" +
                       '"' +
                       self.run +
                       '"' +
                       ', ' +
                       str(int(self.start/self.frq)) +
                       ")'"
                       )

        ovitostring = shlex.split(ovitostring)

        # Compute the MSD with ovito
        cmd = ['python3', '-c']
        cmd.insert(2, ovitostring[0])

        with temp.TemporaryFile() as tempf:
            proc = sub.Popen(cmd, stdout=tempf)
            proc.wait()

        # Change directory to file export directory
        os.chdir(msd_directory)

        # File extension for import
        extension = '_msd.txt'

        msd = []
        step = []

        # Import the data from txt
        with open(self.run+extension) as inputfile:
            for line in inputfile:
                value = line.strip().split(' ')
                step.append(float(value[0]))
                msd.append(float(value[1]))

        # Change back to the first directory
        os.chdir(first_directory)

        pl.plot(step, msd)
        pl.xlabel('Step [-]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.legend([self.run])
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.savefig('../images/motion/'+self.run+'_MSD')
        pl.clf()

        # Return the steps and the msd
        return step, msd

    def rdf(self):
        '''
        Plot the radial distribution at a point and throughout time.
        '''

        # Plot the RDF for a specific timestep
        if self.step is not None:

            # Plot for every step in user input list
            for item in self.step:
                ovitostring = (
                               "'import ovito_rdf as ov; ov.rdfcalc(" +
                               '"' +
                               self.run +
                               '"' +
                               ', ' +
                               str(int(item/self.frq)) +
                               ', ' +
                               str(self.cut) +
                               ', ' +
                               str(self.bins) +
                               ")'"
                               )

                ovitostring = shlex.split(ovitostring)

                # Compute the MSD with ovito
                cmd = ['python3', '-c']
                cmd.insert(2, ovitostring[0])

                with temp.TemporaryFile() as tempf:
                    proc = sub.Popen(cmd, stdout=tempf)
                    proc.wait()

                # File extension for import
                rdffile = rdf_directory+self.run+'_step'+str(item)+'_rdf.txt'

                bins = []
                rdf = []

                # Import the data from txt
                with open(rdffile) as inputfile:
                    for line in inputfile:
                        value = line.strip().split(' ')
                        bins.append(float(value[0]))
                        rdf.append(float(value[1]))

                pl.plot(bins, rdf)
                pl.legend([self.run+'_step_'+str(item)])
                pl.xlabel('Step [-]')
                pl.ylabel('g(r)')
                pl.grid(b=True, which='both')
                pl.tight_layout()
                pl.savefig('../images/rdf/'+self.run+'_'+str(item)+'_rdf')
                pl.clf()

    def response(self):
        '''
        Load the system properties throughout time.
        '''

        # Change into data directory
        os.chdir(data_directory+'../txt/')

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
                           self.run+'.txt',
                           names=mycolumns,
                           sep=' ',
                           comment='#',
                           header=None
                           )

        # Return to the first directory
        os.chdir(first_directory)

        # Plot recorded data versus step
        for item in mycolumns:
            pl.plot(
                    data['Step [-]'],
                    data[item]
                    )
            pl.xlabel('Step [-]')
            pl.ylabel(item)
            pl.legend([self.run])
            pl.grid(b=True, which='both')
            pl.tight_layout()
            pl.savefig(
                       '../images/system/' +
                       self.run +
                       '_' +
                       item.split(' ')[0]
                       )
            pl.clf()

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
                 stepsize,
                 step=None,
                 cut=None,
                 bins=100
                 ):

        '''Load data'''

        self.run = name  # The name of the run
        self.frq = frequency  # The rate of data acquisition
        self.stepsize = stepsize  # The step size used in LAMMPS

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
                       ', ' +
                       str(int(self.stop/self.frq)) +
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

        # Variables to hold data
        data = {}

        # Import the data from txt
        with open(self.run+extension) as inputfile:
            for line in inputfile:
                value = line.strip().split(' ')

                # For each particle type
                for i in range(len(value)):
                    if data.get(i) is None:
                        data[i] = []
                    else:
                        data[i].append(float(value[i]))

        time = [i*self.stepsize for i in data[0]]  # Time from steps
        msd = data[1]  # Total MSD

        data.pop(0)  # Remove time from data
        data.pop(1)  # Remove total MSD from data 

        # Normalize the time
        time = [i-time[0] for i in time]

        # Change back to the first directory
        os.chdir(first_directory)

        for key in data:
            element = key-1
            data[element] = data.pop(key)
            pl.plot(time, data[element], label='Element Type: %i' % element)

        pl.plot(time, msd, label='Total MSD')
        pl.xlabel('Time [ps]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.legend()
        pl.savefig('../images/motion/'+self.run+'_MSD')
        pl.clf()

        # Return the time in pico seconds and the msd
        return time, msd, data

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

        time = [i for i in data['Step [-]']*self.stepsize]

        # Plot recorded data versus step
        for item in mycolumns:
            pl.plot(time, data[item])
            pl.xlabel('Time [ps]')
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

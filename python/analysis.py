from matplotlib import pyplot as pl

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
nei_directory = data_directory + 'neighbor/'


class analize(object):
    '''Computation functions are defined here'''

    def __init__(
                 self,
                 run,
                 start,
                 stop,
                 stepsize,
                 step=None,
                 cut=None,
                 bins=100
                 ):

        '''Load data'''

        self.run = run  # The name of the run
        self.stepsize = stepsize  # The step size used in LAMMPS

        self.frq = par.gather(self.run)  # Rate of data acquisition

        print('Crunching data for ' + self.run)

        self.bins = bins  # The number of bins
        self.cut = cut  # Data for RDF
        self.step = step  # The step to plot RDF

        # Inclusive start and stop conditions
        self.start = start  # Start Step
        self.stop = stop  # Stop step

        # MSD and common neighbor calculations
        ovitostring = (
                       "'import ovito_calc as ov; ov.calc(" +
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

    def msd(self):
        '''
        Plot mean squared displacement.
        '''

        # File extension for import
        extension = '_msd.txt'

        # Variables to hold data
        data = {}

        # Import the data from txt
        with open(msd_directory+self.run+extension) as inputfile:
            for line in inputfile:
                value = line.strip().split(' ')

                # For each particle type
                for i in range(len(value)):
                    if data.get(i) is None:
                        data[i] = []
                    data[i].append(float(value[i]))

        time = [i*self.stepsize for i in data[0]]  # Time from steps
        msd = data[1]  # Total MSD

        data.pop(0)  # Remove time from data
        data.pop(1)  # Remove total MSD from data

        # Normalize the time
        time = [i-time[0] for i in time]

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

    def neighbor(self):
        '''
        Plot the common neighbor analysis.
        '''

        extension = '_neighbor.txt'
        neifile = nei_directory+self.run+extension

        step = []
        fcc = []
        hcp = []
        bcc = []
        ico = []
        with open(neifile) as inputfile:
            for line in inputfile:
                value = line.strip().split(' ')
                step.append(int(value[0]))
                fcc.append(int(value[1]))
                hcp.append(int(value[2]))
                bcc.append(int(value[3]))
                ico.append(int(value[4]))

        time = [i*self.stepsize for i in step]  # Time from steps
        time = [i-time[0] for i in time]  # Normalize the time

        time = np.array(time)
        fcc = np.array(fcc)
        hcp = np.array(hcp)
        bcc = np.array(bcc)
        ico = np.array(ico)

        # Count the number of clusters per time
        fccavg = np.sum(fcc)/time[-1]
        hcpavg = np.sum(hcp)/time[-1]
        bccavg = np.sum(bcc)/time[-1]
        icoavg = np.sum(ico)/time[-1]

        clusters = [fccavg, hcpavg, bccavg, icoavg]

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
        pl.ylabel('[count/ps]')
        pl.grid(b=True, which='both')
        pl.tight_layout()
        pl.savefig('../images/neighbor/'+self.run+'_neighbor')
        pl.clf()

        # Data export
        data = {}
        data['FCC'] = fccavg
        data['HCP'] = hcpavg
        data['BCC'] = bccavg
        data['ICO'] = icoavg

        return data

    def rdf(self):
        '''
        Plot the radial distribution at a point and throughout time.
        '''

        # Plot the RDF for a specific timestep
        if self.step is not None:

            # Plot for every step in user input list
            for item in self.step:

                # Scripts with ovito have to be run separately
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
                pl.xlabel('Bin Center [A]')
                pl.ylabel('g(r)')
                pl.grid(b=True, which='both')
                pl.tight_layout()
                pl.savefig('../images/rdf/'+self.run+'_'+str(item)+'_rdf')
                pl.clf()

    def response(self):
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
                           data_directory+'../txt/'+self.run+'.txt',
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

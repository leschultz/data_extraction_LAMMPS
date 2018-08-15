from matplotlib import pyplot as pl

import dataparse as da
import numpy as np
import os

pl.switch_backend('agg')  # Added for plotting in cluster

# Get relevant directories
first_directory = os.getcwd()
data_directory = first_directory + '/../data/analysis'


class analize(object):
    '''Computation functions are defined here'''

    def __init__(self, name, start, stop):
        '''Load data'''

        self.run = name  # The name of the run

        print('Crunching data for ' + self.run)

        self.rdfout = da.rdf(self.run+'.rdf')  # Load RDF data
        self.bins = self.rdfout[0]  # The number of bins
        self.rdfdata = self.rdfout[1]  # Data for RDF

        self.resout = da.response(self.run+'.txt')  # Load system data

        # Inclusive start and stop conditions
        self.start = start  # Start Step
        self.stop = stop  # Stop step


    def msd(self):
        '''
        Calcualte the means squared displacement.
        '''

        # Compute the MSD with ovito
        command = (
                   "python3 -c 'import ovito_msd as ov; ov.msdcalc(" +
                   '"' +
                   self.run +
                   '"' +
                   ")'"
                   )


        os.system(command)

        # Change directory to file export directory
        os.chdir(data_directory)

        # File extension for import
        extension = '_msd.txt'

        msd = []
        step = []

        # Import the data from txt
        with open(self.run+extension) as inputfile:
            iterlines = iter(inputfile)
            next(iterlines)
            for line in iterlines:
                value = line.strip().split(' ')
                step.append(float(value[0]))
                msd.append(float(value[1]))

        # Change back to the first directory
        os.chdir(first_directory)


        pl.plot(step, msd)
        pl.xlabel('Step [-]')
        pl.ylabel('Mean Squared Displacement [A^2]')
        pl.legend([self.run])
        pl.grid(True)
        pl.tight_layout()
        pl.savefig('../images/motion/'+self.run+'_MSD')
        pl.clf()

        # Return the steps and the msd
        return step, msd

    def rdf(self, step=None):
        '''
        Plot the radial distribution at a point and throughout time.
        '''

        # Gather all the steps where data was recorded
        allsteps = list(set(self.rdfdata.step.values.tolist()))
        allsteps = sorted(allsteps, key=int)

        # The center of bins
        bincenters = list(set(self.rdfdata.center.values.tolist()))
        bincenters = sorted(bincenters, key=float)

        # Plot the data for each bin throughout time
        for i in list(range(1, self.bins+1)):
            index = self.rdfdata.index[self.rdfdata.bins == i].tolist()
            binsdata = self.rdfdata.rdf[index].values.tolist()
            pl.plot(
                    allsteps,
                    binsdata,
                    label="Center [A] %1.2f" % (bincenters[i-1],))

        pl.xlabel('Step [-]')
        pl.ylabel('g(r)')
        pl.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0)
        pl.grid(True)
        pl.tight_layout()
        pl.savefig('../images/rdf/'+self.run+'_allrdf')
        pl.clf()

        # Plot the RDF for a specific timestep
        if step is not None:

            index = self.rdfdata.index[self.rdfdata.step == step].tolist()
            pl.plot(
                    self.rdfdata.center[index],
                    self.rdfdata.rdf[index],
                    )
            pl.legend([self.run+'_step_'+str(step)])
            pl.xlabel('Step [-]')
            pl.ylabel('g(r)')
            pl.grid(True)
            pl.tight_layout()
            pl.savefig('../images/rdf/'+self.run+'_'+str(step)+'_rdf')
            pl.clf()

    def response(self):
        '''
        Plots the response of the system throughout time.
        '''

        # Plot recorded data versus step
        for item in self.resout.columns.values:
            pl.plot(self.resout['Step [-]'], self.resout[item])
            pl.xlabel('Step [-]')
            pl.ylabel(item)
            pl.legend([self.run])
            pl.grid(True)
            pl.tight_layout()
            pl.savefig(
                       '../images/system/' +
                       self.run +
                       '_' +
                       item.split(' ')[0]
                       )
            pl.clf()

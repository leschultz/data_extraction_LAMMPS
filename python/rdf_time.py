from matplotlib import pyplot as pl

import pandas as pd
import numpy as np
import os

#pl.switch_backend('agg')


def rdf_time(name, start, stop):
    '''
    This function averages the rdf peaks between a starting data point and a
    final data point for a specified file defined by name.
    '''

    # Get current directory and the RDF data directory
    first_directory = os.getcwd()
    data_directory = first_directory+'/../data/rdf/'

    # Change to RDF data directory
    os.chdir(data_directory)

    # Grab the number of bins used in LAMMPS
    bin_size = pd.read_csv(name, sep= ' ', skiprows=3, nrows=1, header=None)
    bin_size = bin_size[1][0]

    # Grab the next step where data was aquired
    next_step = pd.read_csv(
                            name,
                            sep= ' ',
                            skiprows=4+bin_size,
                            nrows=1,
                            header=None
                            )

    # The number of rows in the data file (ignores commented rows)
    rows_in_file = len(np.loadtxt(name, usecols=0))

    # the number of data points acquired
    data_chunks = int(rows_in_file/(bin_size+1))


    # Generate list for each bin where g(r) will be stored
    bins = {}
    for i in range(0, bin_size):
        bins[i] = []

    # Gather the data for each acqusition point
    data = {}
    steps = []
    for i in range(0, data_chunks):
        chunk = pd.read_csv(
                            name,
                            sep=' ',
                            skiprows=(1+i*(bin_size+1))+3,
                            nrows=bin_size,
                            header=None
                            )

        chunk = chunk.values

        for j in range(0, bin_size):
            bins[j].append(chunk[j,2])

        steps.append(i*bin_size)

    # The last chunk should contain the bin coordinates
    coordinates = chunk[:,1]

    # Plot each bin with respect to step
    for i in range(0, bin_size):
        pl.plot(steps, bins[i], label="Bin %d"%(i,))

    pl.xlabel('Step [-]')
    pl.ylabel('Bin Center [A]')
    pl.legend(bbox_to_anchor=(1.05,1), borderaxespad=0)
    pl.grid(True)
    pl.tight_layout()
    pl.show()

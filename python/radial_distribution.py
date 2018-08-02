from matplotlib import pyplot as pl

import pandas as pd
import os


def plot(start):
    '''
    This function imports the radial distribution function (RDF) data that
    LAMMPS writes and plots it. The start were data is impored is defined as
    follows:
        Step = 100*100 for a data recording frequency of 100 steps/aquisition
        and an input of 100.
    '''

    # Get directories
    first_directory = os.getcwd()  # Python scripts
    data_directory = first_directory+'/../data/rdf/'
    image_directory = first_directory+'/../images/rdf/'

    # Gather the names of the files in the rdf directory
    file_names = os.listdir(data_directory)

    # Change into the data directory
    os.chdir(data_directory)

    # Import data
    data = {}
    for item in file_names:

        # Gather the number of bins form the last recorded value
        bin_number = pd.read_csv(
                                 item,
                                 sep=' ',
                                 skiprows=3,
                                 nrows=1,
                                 header=None
                                 )

        bin_number = bin_number[1][0]

        # Import from this line in the data file
        line = (start*(bin_number+1))+4

        data[item] = pd.read_csv(
                                 item,
                                 sep=' ',
                                 skiprows=line,
                                 nrows=bin_number,
                                 header=None
                                 )
    # Go to the image save directory
    os.chdir(image_directory)

    # Create a plot for all runs
    print('Plotting the radial distribution function for all in one plot')
    legend_run = []
    for item in data:
        pl.plot(data[item][1], data[item][2])
        legend_run.append(item.split('.')[0])

    pl.xlabel('Center of Bin Coordinate [A]')
    pl.ylabel('g(r)')
    pl.legend(legend_run)
    pl.grid(True)
    pl.savefig('all_rdf.png')
    pl.clf()

    # Create plots for each run
    for item in data:
        print('Plotting the radial distribution function for ' + item)
        pl.plot(data[item][1], data[item][2])
        pl.xlabel('Center of Bin Coordinate [A]')
        pl.ylabel('g(r)')
        pl.legend([item.split('.')[0]])
        pl.grid(True)
        pl.savefig(item.split('.')[0]+'_'+str(start)+'_rdf.png')
        pl.clf()

    # Go back to the first directory
    os.chdir(first_directory)

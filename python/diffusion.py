from numpy.polynomial.polynomial import polyfit

import numpy as np
import os


def diffusion(series, start, stop):
    '''
    Gather the diffusion values for atoms. To run, an average MSD data file is
    needed.
    '''

    # Directory for MSD data
    first_directory = os.getcwd()
    data_directory = first_directory+'/../data/analysis/msd/'

    # Name of file to be imported with absolute path
    name = data_directory+series+'_msd_average.txt'

    data = {}
    with open(name) as inputfile:
        for line in inputfile:
            value = line.strip().split(' ')
            value = [float(i) for i in value]

            for item in list(range(len(value))):
                if data.get(item) is None:
                    data[item] = []
                data[item].append(value[item])

    time = data[0]

    # Find the line of best fit for diffusion
    diffusion = []
    for item in list(range(1, len(data)-1, 2)):
        slope = polyfit(time, data[item], 1)[1]

        # einstein relationship for diffusion
        diffusion.append(slope/6)

    # The output name and location
    output = (
              os.getcwd() +
              '/../data/analysis/diffusion/' +
              series +
              '_diffusion.txt'
              )

    # Save the diffusion data in a txt
    np.savetxt(output, np.transpose(diffusion))

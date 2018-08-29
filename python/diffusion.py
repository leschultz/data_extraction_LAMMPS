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
            if line.startswith('#'):
                header = line.strip().split(' ')
                header.pop(0)
                #newheader = '' 
                #for item in header:
                    #newheader += item+' '
            else:
                value = line.strip().split(',')
                value.pop()
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
              '_diffusion' +
              '_interval(' +
              str(start) +
              '-' +
              str(stop) +
              ').txt'
              )

    fmt = ''
    newheader = ''
    for item in header[1::2]:
        fmt += '%f, '
        newheader += item[:-8]+'[*10^-4 cm^2 s^-1]'+' '

    # Save the diffusion data in a txt
    np.savetxt(output, np.column_stack(diffusion), header=newheader, fmt=fmt)

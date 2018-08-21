from numpy.polynomial.polynomial import polyfit

import averages as av
import numpy as np
import os


def diffusion(*args, **kwargs):
    '''Gather the diffusion values for atoms'''

    # Pass all agruments into averages.py
    value = av.avg(*args, **kwargs)

    # Grab the name of the temperature runs used
    series = args[0]+'_diffusion.txt'

    # Gather all the outputs from averages.py
    time = value[0]
    msd_all = value[1]
    msd_all_eim = value[2]
    msd_type = value[3]
    msd_type_eim = value[4]

    # Find a line of best fit for all diffusion
    m = polyfit(time, msd_all, 1)[1]

    # Find the line of best fit for diffusion for each element type
    diff_types = {}
    order = []
    for key in msd_type:
        order.append(key)
        slope = polyfit(time, msd_type[key], 1)[1]
 
        if diff_types.get(key) is None:
            diff_types[key] = []
    
        # einstein relationship for diffusion
        diff_types[key].append(slope/6)

    diff_all = m/6  # Diffusion for all atoms

    # The output name and location
    output = (
              os.getcwd() +
              '/../data/analysis/diffusion/' +
              series
              )

    # Data to be exported
    columns = [diff_all]

    # Grab the diffusion values for each type in columns
    order.sort()  # Gather dictionary types in order of element type
    for item in order:
        columns.append(diff_types[item][0])

    # Save the diffusion data in a txt
    np.savetxt(output, columns)

'''
This script imports diffusion data calculated for error propagation.
'''

import pandas as pd
import os


def diffusionimport(maindir):
    '''
    Gather caluclated diffusion data and export it.

    inputs:
            maindir = the main directory where all runs are stored
    outputs:
            datasets = a dictionary containing all diffusivity data
    '''

    folders = os.listdir(maindir)  # List all runs

    # Iterate over all runs in a directory.
    data = {}
    for folder in folders:
        data[folder] = {}

        # List files in the main directory for each run
        filepath = maindir+'/'+folder+'/datacalculated/diffusion/'
        files = os.listdir(filepath)

        # origins denotes multiple origins (MO) data while regular is the
        # diffusion from a single linear interpolation.
        origins = [filepath+i for i in files if 'origin' in i]
        regular = [filepath+i for i in files if 'origin' not in i]

        data[folder]['origins'] = origins
        data[folder]['regular'] = regular

    # Iterate through files and determine which is MO vs regular
    datasets = {}
    for key in data:
        datasets[key] = {'origins': {}, 'regular': {}}
        for item in data[key]:
            for name in data[key][item]:
                if 'origins' in item:
                    temp = name.split('_')[-2]

                if 'regular' in item:
                    temp = name.split('_')[-1]

                # Export diffusivity data into pandas data frame
                temp = float(temp[:-1])
                df = pd.read_csv(name, sep=' ')
                datasets[key][item][temp] = df

    return datasets

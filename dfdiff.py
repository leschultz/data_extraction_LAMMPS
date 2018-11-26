from matplotlib import pyplot as pl
from scipy import stats as st

from diffusionimport import load
from matplotlib import lines
from itertools import islice

from ukuiestimator import error as ukui
from batchmeans import error as batch

import pandas as pd
import numpy as np
import os


def diffusionimport(maindir):
    folders = os.listdir(maindir)

    data = {}
    for folder in folders:
        data[folder] = {}

        filepath = maindir+folder+'/datacalculated/diffusion/'
        files = os.listdir(filepath)

        origins = [filepath+i for i in files if 'origin' in i]
        regular = [filepath+i for i in files if 'origin' not in i]

        data[folder]['origins'] = origins
        data[folder]['regular'] = regular

    datasets = {}
    for key in data:
        datasets[key] = {'origins': {}, 'regular': {}}
        for item in data[key]:
            for name in data[key][item]:
                if 'origins' in item:
                    temp = name.split('_')[-2]

                if 'regular' in item:
                    temp = name.split('_')[-1]

                temp = float(temp[:-1])
                df = pd.read_csv(name, sep= ' ')
                datasets[key][item][temp] = df

    return datasets

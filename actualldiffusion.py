from diffusionimport import load
from matplotlib import pyplot as pl
from scipy.stats import sem

import numpy as np
import os

def actual(path):
    folders = os.listdir(path)

    diffusions = []
    for folder in folders:
        newpath = path+'/'+folder+'/datacalculated/diffusion/'
        files = os.listdir(newpath)

        for item in files:
            diffusions.append(newpath+item)

    x = []
    for item in diffusions:
        if 'origins' not in item:
            x.append(item)

    data = {}
    for item in x:
        with open(item) as file:
            temp = float(item.split('_')[-1][:-1])

            if data.get(temp) is None:
                data[temp] = []

            next(file)
            for line in file:
                value = line.strip().split(' ')
                data[temp].append(float(value[0]))

    newdata = {}
    for key in data:
        newdata[key] = np.mean(data[key])
        newdata[str(key)+'_err'] = sem(data[key])

    return newdata

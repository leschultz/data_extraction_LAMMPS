'''
Katzgraber, H. G. (2009). Introduction to Monte Carlo Methods.
Retrieved from http://arxiv.org/abs/0905.1629
'''

from matplotlib import pyplot as pl
from diffusionimport import load

import numpy as np
import os


def correlation(x, l):
    '''
    Calculate the autocorrelation at different lengths.
    '''

    n = len(x)
    mean = np.mean(x)

    val = 0
    for i in range(0, n-l):
        val += x[i]*x[i+l]-mean**2

    val /= n-l

    return val


def standarderror(x):
    '''
    Return the standard error based on variance.
    '''

    n = len(x)

    val = 0
    for i in range(0, n):
        for j in range(0, n):
            val += sum(autocorrelation(x)[1])

    val /= n**2
    val **= 0.5
    val /= n**0.5

    return val

def autocorrelation(x):
    '''
    Use correlation value for l
    '''

    N = len(x)
    l = list(range(0, N-1))

    values = []
    lout = []
    for i in l:
        value = correlation(x, i)

        if value >= 0:
            values.append(value)
            lout.append(i)

    return lout, values

directory = '../export/4000atom545000/datacalculated/diffusion/'

runs = os.listdir(directory)

for run in runs:
    if 'origins' in run:
        print(run)
        data = load(directory+run, ' ')

        temp = run.split('_')[-2]
        err = standarderror(data['all'])
        print(err)

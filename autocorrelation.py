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

    val = 0
    for i in range(0, n-l):
        val += x[i]*x[i+l]-np.mean(x)**2

    val /= n-l

    return val


def standarderror(x, l):
    '''
    Return the standard error based on variance.
    '''

    n = len(x)

    val = 0
    for i in range(0, n):
        for j in range(0, n):
            val += autocorrelation(x, l)

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
    for i in l:
        values.append(correlation(x, i))

    return l, values

directory = '../export/4000atom545000/datacalculated/diffusion/'

runs = os.listdir(directory)
print(runs)

for run in runs:
    if 'origins' in run:
        data = load(directory+run, ' ')

        temp = run.split('_')[-2]
        l, values = autocorrelation(data['all'])
        # pl.plot(l, values, label=temp)

# pl.legend(loc='best')

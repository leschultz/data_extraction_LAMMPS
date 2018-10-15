'''
Katzgraber, H. G. (2009). Introduction to Monte Carlo Methods.
Retrieved from http://arxiv.org/abs/0905.1629
'''

from matplotlib import pyplot as pl
from diffusionimport import load

import numpy as np
import os


def autocorrelation(x, l):
    '''
    Calculate the autocorrelation at different lengths.
    '''

    n = len(x)
    meansquared = np.mean(x)**2

    val = 0
    for i in range(0, n-l):
        val += x[i]*x[i+l]-meansquared

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
    val /= n
    val **= 0.5

    return val

def correlationlength(x):
    '''
    Use correlation value for l
    '''

    N = len(x)
    l = list(range(0, N-1))

    values = []
    lout = []
    for i in l:
        lout.append(i)
        values.append(autocorrelation(x, i))

    count = 0
    for i in values:
        if i > 0:
            lcut = lout[count]
        else:
            break

        count += 1

    return lout, values, lcut

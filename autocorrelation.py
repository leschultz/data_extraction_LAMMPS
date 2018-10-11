'''
Katzgraber, H. G. (2009). Introduction to Monte Carlo Methods.
Retrieved from http://arxiv.org/abs/0905.1629
'''

from matplotlib import pyplot as pl
from diffusionimport import load

import numpy as np
import os


def autocorrelationvan(x, l):
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


def standarderrorvan(x):
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

def correlationvanlength(x):
    '''
    Use correlation value for l
    '''

    N = len(x)
    l = list(range(0, N-1))

    values = []
    lout = []
    for i in l:
        value = correlation(x, i)
        lout.append(i)
        values.append(value)

    return lout, values



def autocorrelation(x, l):
    '''
    Calculate the autocorrelation at different lengths.
    '''

    n = len(x)
    mean = np.mean(x)

    val = 0
    for i in range(0, n-l):
        val += (x[i]-mean)*(x[i+l]-mean)

    val /= n-l

    return val


def standarderror(x, lcut):
    '''
    Return the standard error based on variance.
    '''

    n = len(x)

    val = 0
    for i in range(0, n):
        for j in range(0, n):
            val += autocorrelation(x, lcut)

    val /= n**2
    val **= 0.5
    val /= n**0.5

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
        value = autocorrelation(x, i)
        lout.append(i)
        values.append(value)
        if value > 0:
            lcut = i

    return lout, values, lcut

'''
directory = '../export/4000atom545000/datacalculated/diffusion/'

runs = os.listdir(directory)

for run in runs:
    if 'origins' in run:
        print(run)
        data = load(directory+run, ' ')

        temp = run.split('_')[-2]
        lout, values, lcut = correlationlength(data['all'])
        val = standarderror(data['all'], lcut)
        print(val)

        pl.plot(lout, values, '.', label=temp)


pl.xlabel('l measurements appart')
pl.ylabel('V(l) [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.tight_layout()
pl.grid()
pl.savefig('../autocorrelation')
pl.show()
pl.clf()
'''

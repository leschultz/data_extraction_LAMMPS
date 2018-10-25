import numpy as np


def selfcovariance(x):
    '''
    Calculate the autocorrelation at different lengths.
    '''

    n = len(x)
    average = np.mean(x)

    val = 0.0
    for i in range(0, n):
        val += (x[i]-average)**2

    val /= n-1

    return val


def standarderror(x):
    '''
    Return the standard error based on variance.
    '''

    n = len(x)

    cov = selfcovariance(x)

    val = 0.0
    for i in range(0, n):
        for j in range(0, n):
            val += cov

    val /= n**2.0
    val /= n
    val **= 0.5

    return val

def variance(x, y):
    '''
    Return the variance of the data.
    '''

    n = len(x)

    if n != len(y):
        raise ValueError('Both arrays are not the same length')

    val = 0.0
    for i in range(0, n):
        for j in range(i+1, n):
            val += (x[i]-x[j])*(y[i]-y[j])

    val /= n**3
    val **= 0.5

    return val

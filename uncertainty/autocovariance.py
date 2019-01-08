'''
This scripts computes the autocorrelation function for different k-lags.
'''

import numpy as np


def autocovariance(x, n, k, mean):
    '''
    Compute the autocovariance of a set.

    inputs:
            x = the list of data
            n = the size of data
            k = the k-lag between values
            mean = the mean of the x-data

    outputs:
            autocov = the autocovariance at a k-lag
    '''

    autocov = 0.0
    for i in np.arange(0, n-k):
        autocov += (x[i+k]-mean)*(x[i]-mean)

    autocov *= (1/(n-1))  # Need two values or more for this to work

    return autocov


def auto(x):
    '''
    Compute the autocorrelation for all possible k-lags.

    inputs:
            x = the data
    outputs:
            k = the distance between x indexes (k-lag)
            r = the autocorrelation at a k-lag
            last = the last index before r becomes zero or negative
    '''

    n = len(x)
    mean = np.mean(x)

    denominator = autocovariance(x, n, 0, mean)

    k = []
    r = []
    numerator = []
    for i in np.arange(0, n+1):
        k.append(i)
        r.append(autocovariance(x, n, i, mean)/denominator)

    count = 0
    for i in r:
        if i >= 0.0:
            last = count
            count += 1
        else:
            break

    return k, r, last

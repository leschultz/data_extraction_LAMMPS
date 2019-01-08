'''
This scripts computes the autocorrelation function for different k-lags.
'''

import numpy as np


def autocovariance(x, n, k, mean, bias=0.0):
    '''
    Compute the autocovariance of a set.

    inputs:
            x = the list of data
            n = the size of data
            k = the k-lag between values
            mean = the mean of the x-data
            bias = adjust the bias calculation

    outputs:
            autocov = the autocovariance at a k-lag
    '''

    autocov = 0.0
    for i in np.arange(0, n-k):
        autocov += (x[i+k]-mean)*(x[i]-mean)

    autocov /= n-bias

    return autocov

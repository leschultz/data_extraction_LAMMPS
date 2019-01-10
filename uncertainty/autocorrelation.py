'''
This scripts computes the autocorrelation function for different k-lags.
'''

import numpy as np

from uncertainty.autocovariance import autocovariance


def autocorrelation(x):
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

    # Find the last index before r becomes zero
    count = 0
    for i in r:
        if i >= 0.0:
            last = count
            count += 1
        else:
            break

    return k, r, last

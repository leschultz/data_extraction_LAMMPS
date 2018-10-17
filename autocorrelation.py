import numpy as np


def autocorrelation(x, l):
    '''
    Calculate the autocorrelation at different lengths.
    '''

    n = len(x)
    minusl = n-l

    val = 0
    for i in range(0, minusl):
        val += x[i]*x[i+l]

    val /= minusl
    val -= np.mean(x)**2.0

    return val


def standarderror(x, l):
    '''
    Return the standard error based on variance.
    '''

    n = len(x)

    covariance = autocorrelation(x, l)

    val = 0
    for i in range(0, n):
        for j in range(0, n):
            val += covariance

    val /= n**2.0
    val /= n
    val **= 0.5

    return val


def correlationlength(x):
    '''
    Use correlation value for l
    '''

    n = len(x)
    lvals = list(range(0, n-1))

    values = []
    lout = []
    for i in lvals:
        lout.append(i)
        values.append(autocorrelation(x, i))

    # Find where the autocorrelation first comes close to zero
    count = 0
    for i in values:
        if i >= 0:
            lcut = lout[count]
            count += 1

        else:
            break

    return lout, values, lcut

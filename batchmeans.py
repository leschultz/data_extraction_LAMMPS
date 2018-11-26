'''
This method used the batch means.
A standard recomendation is block size sqrt(n).

Source:
@article{,
file = {:home/nerve/Documents/UW/Papers/batchmeans.pdf:pdf},
mendeley-groups = {Monte Carlo},
pages = {95--95},
title = {{Batch means standard errors for MCMC}},
year = {2005}
}
'''

import math


def error(x, a=None, b=None):
    n = len(x)
    mean = sum(x)/n

    if a is None:
        a = math.floor(n/b)

    if b is None:
        b = math.floor(n/a)

    averages = []
    for k in range(0, a):
        val = 0.0
        for i in range(k*b, (k+1)*b):
            val += x[i]

        val /= b
        averages.append(val)

    val = 0.0
    for i in range(0, a):
        val += (averages[i]-mean)**2.0

    val /= a-1
    val *= b

    sigma = val**0.5
    standarderror = sigma/(n**0.5)

    return standarderror

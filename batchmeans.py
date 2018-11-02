'''
This method used the batch means.
A standard recomendation is block size 10.

Source:
http://www.stat.umn.edu/geyer/5102/notes/mcmc.pdf
'''

import math


def error(x, a=10):
    n = len(x)
    mean = sum(x)/n

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
    standarderror = sigma/(a**0.5)

    return standarderror

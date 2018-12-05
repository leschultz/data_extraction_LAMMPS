'''
This method used the batch means.
'''

import numpy as np


def error(x, a=None, b=None):
    n = len(x)

    if a is None:
        a = n//b

    if b is None:
        b = n//a

    blocks = np.array_split(x, a)

    averages = [np.mean(i) for i in blocks]

    variance = np.var(averages, ddof=1)
    standarderror = (variance/a)**0.5

    return standarderror, a

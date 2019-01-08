'''
This method used the batch means to calculate uncertainty and an average.
'''

import numpy as np


def error(x, a=None, b=None):
    '''
    Divide data defined by either number of blocks or approximate block
    length. Then, uncertainty and an average is calculated for the smple.

    inputs:
            x = the data set
            a = the number of blocks
            b = the number of items in each block approximately
    outputs:
            standarderror = error using bins
            a = the number of blocks if it was not defined
    '''

    n = len(x)  # Length of sample

    # Find a if b is defined
    if a is None:
        a = n//b  # Division that removes remainder

    # Find b if a is defined
    if b is None:
        b = n//a  # Division that removes remainder

    blocks = np.array_split(x, a)  # Divide dat into blocks

    averages = [np.mean(i) for i in blocks]  # Mean for each block

    variance = np.var(averages, ddof=1)  # The variance of block means
    standarderror = (variance/a)**0.5  # Standard error in the mean

    return standarderror, a

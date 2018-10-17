import numpy as np


def block(data, n=10):
    '''
    Devides the data into ten portions (default) do do block averaging.
    '''

    # Divide the data into blocks
    blocks = [data[i::n] for i in range(n)]

    # Average the blocks and find their error in the mean
    averages = [np.mean(i) for i in blocks]
    value = np.mean(averages)
    eim = np.std(averages)
    eim /= len(averages)**0.5

    return value, eim

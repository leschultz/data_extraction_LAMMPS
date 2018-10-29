import numpy as np


def block(data, n=10):
    '''
    Devides the data into ten portions (default) to do block averaging.
    '''

    # Divide the data into blocks
    blocks = [data[i::n] for i in range(n)]

    # Average the blocks and find their error in the mean
    averages = [sum(i)/len(i) for i in blocks]
    n = len(averages)
    mean = sum(averages)/n

    # The standard deviation
    sigma = np.std(averages)
    eim = sigma/(n**0.5)

    return mean, eim

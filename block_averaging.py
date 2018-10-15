from scipy import stats as st

import numpy as np


def block(data, n=10):
    '''
    Devides the data into ten portions (default) do do block averaging.
    '''

    # Divide the data into blocks
    blocks = [data[i::n] for i in range(n)]

    # Average the blocks and find their error in the mean
    averages = np.mean(blocks)
    eim = st.sem(blocks, axis=None)

    return averages, eim

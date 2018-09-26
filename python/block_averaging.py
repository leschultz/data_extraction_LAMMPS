from scipy import stats as st

import numpy as np


def block_averaging(data):
    '''
    Devides the data into ten portions do do block averaging.
    '''

    N = 10  # Number of blocks
    length = len(data['time'])  # The data length
    half = length//10  # Divide indexes but removes point if remainder exists

    blocks = list(range(0, length, half))  # Index intervals

    # Filter the data
    del data['time']

    # The following delete lines remove the error from linear fits
    delete = []
    for key in data:
        if '_Err' in key:
            delete.append(key)

    for key in delete:
        del data[key]

    # Divide the data into blocks
    block_data = {}
    for key in data:
        count = 0
        for block in blocks[:-1]:
            start = blocks[count]
            end = blocks[count+1]

            name = key+'_'+str(count)
            block_data[name] = data[key][start:end]

            count += 1

    # Grab the keys for data
    keys = list(data.keys())

    # Grab averages of each block
    values = {}
    for key in keys:
        values[key] = []

    count = 0
    for key in block_data:
        for item in keys:
            if item in key:
                values[item].append(np.mean(block_data[key]))

        count += 1

    averages = {}
    for key in values:
        averages[key] = np.mean(values[key])
        averages[key+'_err'] = st.sem(values[key])

    return averages 

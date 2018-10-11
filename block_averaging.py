from scipy import stats as st

import numpy as np


def block_averaging(data0, n=10):
    '''
    Devides the data into ten portions (default) do do block averaging.
    '''

    # Prevent actual deletion of original data input
    data = {}
    for key in data0:
        data[key] = data0[key]

    # Filder the data
    del data['start_time']

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
        dat = data[key]
        blocktemp = [dat[i:i+n] for i in range(0, len(dat), n)]

        count = 0
        for b in blocktemp:
            name = key+'_'+str(count)
            block_data[name] = blocktemp[count]

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

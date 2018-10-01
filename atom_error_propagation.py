from scipy import stats as st

import numpy as np


def diffusion(data):
    '''
    Propagate error from the standard error of atomic positions.
    '''

    time = data['time']

    del data['time']

    diff = {}
    for key in data:
        if '_EIM' not in key:
            upper = np.array(data[key])+np.array(data[key+'_EIM'])
            lower = np.array(data[key])-np.array(data[key+'_EIM'])

            upper = list(upper)
            lower = list(lower)

            up = st.linregress(time, upper)
            lo = st.linregress(time, lower)

            diffup = up[0]/6
            diffdo = lo[0]/6

            diff[key+'_err'] = diffup-diffdo

    return diff

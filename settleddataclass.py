from scipy import stats as st
from autocovariance import auto

import pandas as pd
import numpy as np


def ptest(x, nullhyp, a, test, alpha=0.05, n0=5):
    '''
    Find the p-values for each bin with respect to the last bin.

    inputs:
            x = binned data
            nullhyp = null hypothesis
            a = the number of bins
            alpha = the significance level
            n0 = the threshold for the number of agreements with nullhyp
    outputs:
            pvals = p-values for each bin with respect to the last bin
            index = last bin where the p-values is less than alpha
            alpha = return alpha if default is used
    '''

    # Store the bin where p-value is less than alpha
    onoff = np.zeros(a, dtype=int)

    pvals = []
    for i in x:
        if test == 'distribution':

            pvals.append(
                         st.ttest_ind(i, nullhyp, equal_var=False)[1]
                         )

        if test == 'single':
            pvals.append(st.ttest_1samp(i, nullhyp)[1])

    count = 0
    indexes = []
    for i in pvals:
        if i <= alpha:
            onoff[count] = 1
            indexes.append(count)

        count += 1

    # Count the number of ones within n0 blocks from each other
    diff = []
    index = 0
    for x, y in zip(indexes, indexes[1:]):
        operation = y-x  # Find the number of 0's between 1
        if operation <= n0:
            index = y

    # If the first index returns 0, then check for first instance of fail
    if (index == 0) & (sum(onoff) > 0):
        index = np.where(onoff == 1)[0]
        index = min(index)
        index += 1

    elif sum(onoff) == 0:
        index = 0
    else:
        index += 1  # Skip problematic bin

    return pvals, index


class settled(object):
    '''
    Class to grab the indexes of settled data based on slopes per bin.
    Data has to be sufficiently long to not breack this code.
    '''

    def __init__(self, x, y, alpha=0.05, n0=5):
        '''
        Devide data into a number of bins.

        inputs:
                x = x-axis data
                y = y-axis data
                n = length of x values
                a = number of bins
                b = length of bins (approximate)
                n = length of x values
        '''

        self.x = x
        self.y = y
        self.n = len(x)

        self.alpha = alpha  # Defined under ptest function
        self.n0 = n0  # Defined under ptest function

        self.binselect = {}  # Store selected bin
        self.indexes = {}  # Store first index of selected bin

    def binsize(self):
        '''
        Use autocorrelation function to find correlation length.

        inputs:
                self.yblocks = y-axis data
        outputs:
                b = length of bins (approximate)

        '''

        k, r, index = auto(self.y)

        if index <= 2:
            index = 4
        else:
            index *= 2

        self.b = index

        return self.b

    def batch(self):
        '''
        Devide data into a number of bins.

        inputs:
                b = minimum bin length
        outputs:
                blocks = binned data
        '''

        # Estimate the number of bins from block length
        self.a = self.n//self.b

        self.xblocks = np.array_split(self.x, self.a)
        self.yblocks = np.array_split(self.y, self.a)

        return self.xblocks, self.yblocks

    def binslopes(self):
        '''
        Linear regression for each block of data.
        Data blocks must be same for both x and y.

        inputs:
                self.xblocks = binned x-axis data
                self.yblocks = binned y-axis data
        outputs:
                self.slopes = slopes for each bin
                self.err = error from fitting
        '''

        slopes = []
        errs = []
        for j in range(0, self.a):
            fit = st.linregress(self.xblocks[j], self.yblocks[j])
            slopes.append(fit[0])
            errs.append(fit[-1])

        self.blockslopes = slopes
        self.errs = errs

        return self.blockslopes, self.errs

    def binnedslopetest(self):
        '''
        Find the index of data where.

        inputs:
                self.slopes = binned slope data
        outputs:
                self.blockslopes = the slope for bins
                i = the first slope value fitting criteria
        '''

        n = self.n-1

        try:
            # If the start is decreasing
            if self.blockslopes[1]-self.blockslopes[0] < 0.0:
                for i in range(0, n):
                    if self.blockslopes[i+1]-self.blockslopes[i] > 0.0:
                        break

            # If the start is increasing
            elif self.blockslopes[1]-self.blockslopes[0] > 0.0:
                for i in range(0, n):
                    if self.blockslopes[i+1]-self.blockslopes[i] < 0.0:
                        break

            else:
                i = 0

        except Exception:
            i = 'NA'

        self.binselect['binned slopes'] = i

        return self.blockslopes, i

    def ptests(self, expected):
        '''
        Find the p-values for each bin with respect to the last bin.

        inputs:
                self.yblocks = binned y-axis data
                alpha = the significance level
        outputs:
                pvals = p-values for each bin with respect to the last bin
                index = last bin where the p-values is less than alpha
        '''

        distpvals, index = ptest(
                                 self.yblocks,
                                 self.yblocks[-1],
                                 self.a,
                                 'distribution',
                                 self.alpha
                                 )

        keydistpvals = r'p-value from distribution ($\alpha$='+str(self.alpha)+')'
        self.binselect[keydistpvals] = index

        singpvals, index = ptest(
                                 self.yblocks,
                                 expected,
                                 self.a,
                                 'single',
                                 self.alpha
                                 )

        keysingpvals = r'p-value from single sample ($\alpha$='+str(self.alpha)+')'
        self.binselect[keysingpvals] = index

        self.distpvals = distpvals
        self.singpvals = singpvals

        return distpvals, singpvals

    def normaldistribution(self):
        '''
        Check whether a slope observation is outside the confidence interval
        of a normal distribution.

        inputs:
                alpha = the significance level
                self.blockslopes = the bins with linear fits
        outputs:
                failbins = The bins that fail the test
        '''

        failbins = []
        count = 0
        ppf = []
        for i in self.blockslopes:
            # The minimum absolute value before going outside 2*sigma
            # The 2*sigma is defined by 1-alpha and can be altered
            limit = st.norm.ppf(1-self.alpha, i, self.errs[count])
            ppf.append(limit)

            if (0.0 <= -limit) | (0.0 >= limit):
                failbins.append(count)

            count += 1

        # Choose the first bin where data failed
        if failbins:
            index = min(failbins)
            index += 1  # Choose the next bin as being settled

        else:
            index = 0

        self.binselect['slope confidence interval '+str(1-self.alpha)] = index
        self.ppf = ppf

        return ppf

    def finddatastart(self):
        '''
        Find the start of settled data.

        inputs:
                self.yblocks = binned y-axis data
        outputs:
                index = the starting index of settled data
        '''

        for key in self.binselect:
            try:
                index = sum([
                             len(j) for j in self.yblocks[:self.binselect[key]]
                             ])

                self.indexes[key] = index

            except Exception:
                self.indexes[key] = 'NA'

        return self.indexes

    def returndata(self):
        bins = list(range(0, self.a))

        data = [
                bins,
                self.blockslopes,
                self.distpvals,
                self.singpvals,
                self.ppf
                ]

        headers = [
                   'bin',
                   'blockslopes',
                   'distpvals',
                   'singpvals',
                   'ppf'
                   ]

        df = pd.DataFrame(np.array(data).T, columns=headers)
        df['bin'] = df['bin'].astype(int)

        return df

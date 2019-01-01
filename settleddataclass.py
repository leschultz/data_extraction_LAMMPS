'''http://iaingallagher.tumblr.com/post/50980987285/t-tests-in-python'''

from scipy import stats as st
from autocovariance import auto
from matplotlib import pyplot as pl

import pandas as pd
import numpy as np


def ptest(x, nullhyp, a, alpha=0.05, n0=5):
    '''
    Find the p-values for each bin with respect to the last bin.

    inputs:
            x = binned data
            nullhyp = null hypothesis
            a = the number of bins
            alpha = the significance level
            n0 = the threshold for then number of agreements with nullhyp
    outputs:
            pvals = p-values for each bin with respect to the last bin
            index = last bin where the p-values is less than alpha
            alpha = return alpha if default is used
    '''

    # Store the bin where p-value is less than alpha
    onoff = np.zeros(a, dtype=int)

    pvals = []
    for i in x:
        pvals.append(
                     st.ttest_ind(i, nullhyp, equal_var=False)[1]
                     )

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

    return pvals, index, alpha


class settled(object):
    '''
    Class to grab the indexes of settled data based on slopes per bin.
    Data has to be sufficiently long to not breack this code.
    '''

    def __init__(self, x, y):
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

        if index < 3:
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

    def slopetest(self):
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

        self.binselect['slope'] = i

        return self.blockslopes, i

    def ptestblock(self, alpha=0.05):
        '''
        Find the p-values for each bin with respect to the last bin.

        inputs:
                self.yblocks = binned y-axis data
                alpha = the significance level
        outputs:
                pvals = p-values for each bin with respect to the last bin
                index = last bin where the p-values is less than alpha
        '''

        pvals, index, alpha = ptest(
                                    self.yblocks,
                                    self.yblocks[-1],
                                    self.a,
                                    alpha
                                    )

        self.binselect['p'] = index

        return pvals, index, alpha

    def ptestfit(self, expected, withinfraction=0.0005):
        '''
        Settling criterion due to liner fitting error.

        inputs:
                self.x = horizontal axis values
                self.y = vertical axis values
                expected = the expected value
                withinfraction = the decimal range to stay within expected
        outputs:
                slopes = linear regression starting from end of data
                averages = averages starting from the end of data
                index = the starting index of settled data
        '''

        # Need at least two points for linear regression
        slopes = []
        averages = []
        indexes = []
        for i in range(self.n-2, -1, -1):
            indexes.append(i)
            x = self.x[i:]
            y = self.y[i:]
            averages.append(sum(self.y[i:])/len(self.y[i:]))
            fit = st.linregress(x, y)
            slopes.append(fit[0])

        upper = expected*(1+withinfraction)
        lower = expected*(1-withinfraction)

        averages = np.array(averages)

        try:
            start = min(np.where((averages <= upper) & (averages >= lower))[0])

            posslopes = [abs(i) for i in slopes]
            slopestart = posslopes.index(min(posslopes[start:]))
            index = indexes[slopestart]

        except Exception:
            index = 'NA'
            start = 'NA'
            slopestart = 'NA'

        self.indexes['fiterror'] = index

        return slopes, averages, index, start, slopestart

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

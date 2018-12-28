from scipy import stats as st
from autocovariance import auto

import numpy as np


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
            if self.blockslopes[1]-self.blockslopes[0] > 0.0:
                for i in range(0, n):
                    if self.blockslopes[i+1]-self.blockslopes[i] < 0.0:
                        break

        except Exception:
            i = 'NA'

        self.binselect['slope'] = i

        return self.blockslopes, i

    def ptest(self, alpha=0.05):
        '''
        Find the p-values for each bin with respect to the last bin.

        inputs:
                self.yblocks = binned y-axis data
                alpha = the significance level
        outputs:
                pvals = p-values for each bin with respect to the last bin
                index = last bin where the p-values is less than alpha
        '''

        pvals = []
        for i in self.yblocks:
            pvals.append(
                         st.ttest_ind(i, self.yblocks[-1], equal_var=False)[1]
                         )

        count = 0
        indexes = []
        for i in pvals:
            if i < alpha:
                indexes.append(count)

            count += 1

        if indexes:
            index = min(indexes)
            if index < self.a:
                index += 1  # Skip the problematic bin
            else:
                index = 'NA'

        else:
            index = 'NA'

        self.binselect['p'] = index

        return pvals, index

    def fittest(self):
        '''
        Settling criterion due to liner fitting error.

        inputs:
                self.blockslopes = slopes of bins
                self.errs = slope errors from bins
        outputs:
                self.errs = slope errors from bins
                index = first index where slope error exceeds std
        '''

        fit = st.linregress(self.x, self.y)
        slope = fit[0]
        err = fit[-1]

        indexes = []
        count = 0
        for i in self.errs:
            if i < err:
                indexes.append(count)

            count += 1

        try:
            index = min(indexes)
        except Exception:
            index = 'NA'

        self.binselect['fiterror'] = index

        return self.errs, index

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

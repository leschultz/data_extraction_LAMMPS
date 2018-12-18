from scipy import stats as st

import numpy as np


class settled(object):
    '''
    Class to grab the indexes of settled data based on slopes per bin.
    '''

    def __init__(self, x, y, a=None, b=None):
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
        self.a = a
        self.b = b
        self.binselect = {}
        self.indexes = {}

    def batch(self):
        '''
        Devide data into a number of bins.

        inputs:
                a = number of bins
                b = length of bins (approximate)
        outputs:
                blocks = binned data
                a = number of bins
        '''

        # Estimate the number of bins from block length
        if self.a is None:
            self.a = self.n//self.b

        # Estimate the block length from the number of bins
        if self.b is None:
            self.b = self.n//self.a

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

    def findslopestart(self):
        '''
        Find the index of data where

        inputs:
                self.slopes = binned slope data
        outputs:
                i = the first slope value fitting criteria
        '''

        n = self.n-1

        # If the start is decreasing
        if self.blockslopes[1]-self.blockslopes[0] < 0.0:
            for i in range(0, n):
                if self.slopes[i+1]-self.slopes[i] > 0.0:
                    break

        # If the start is increasing
        if self.blockslopes[1]-self.blockslopes[0] > 0.0:
            for i in range(0, n):
                if self.blockslopes[i+1]-self.blockslopes[i] < 0.0:
                    break

        self.binselect['slope'] = i

        return i

    def ptest(self, alpha=0.05):
        '''
        Find the p-values for each bin with respect to the last bin

        inputs:
                self.yblocks = binned y-axis data
                alpha = the significance level
        outputs:
                index = The last bin where the p-values is less than alpha
        '''

        pvals = [
                 st.ttest_ind(i, self.yblocks[-1],
                 equal_var=False)[1] for i in self.yblocks
                 ]

        count = 0
        indexes = []
        for i in pvals:
            if i < alpha:
                indexes.append(count)

            count += 1

        index = min(indexes)
        index += 1  # Skip the problematic bin
        self.binselect['p'] = index

        return index

    def finddatastart(self):
        '''
        Find the start of settled data

        inputs:
                self.yblocks = binned y-axis data
        outputs:
                index = the starting index of settled data
        '''

        for key in self.binselect:
            index = sum([len(j) for j in self.yblocks[:self.binselect[key]]])
            self.indexes[key] = index

        return self.indexes

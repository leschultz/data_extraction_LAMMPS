from scipy import stats as st

import numpy as np


class settled(object):
    '''
    Class to grab the indexes of settled data based on slopes per bin.
    '''

    def batch(self, x, a=None, b=None):
        '''
        Devide data into a number of bins.

        inputs:
                a = number of bins
                b = length of bins (approximate)
        outputs:
                blocks = binned data
                a = number of bins
        '''

        n = len(x)

        # Estimate the number of bins from block length
        if a is None:
            a = n//b

        # Estimate the block length from the number of bins
        if b is None:
            b = n//a

        blocks = np.array_split(x, a)

        return blocks, a

    def binslopes(self, x, y, bins):
        '''
        Linear regression for each block of data.
        Data blocks must be same for both x and y.

        inputs:
                x = binned x-axis data
                y = binned y-axis data
        outputs:
                slope = slopes for each bin
        '''

        slope = []
        for j in range(0, len(x)):
            slope.append(np.polyfit(x[j], y[j], 1)[0])

        return slope

    def findslopestart(self, x):
        '''
        Find the index of data where

        inputs:
                x = binned x data
        outputs:
                i = the first slope value fitting criteria
        '''
        n = len(x)-1

        # If the start is decreasing
        if x[1]-x[0] < 0.0:
            for i in range(0, n):
                if x[i+1]-x[i] > 0.0:
                    break

        # If the start is increasing
        if x[1]-x[0] > 0.0:
            for i in range(0, n):
                if x[i+1]-x[i] < 0.0:
                    break

        return i

    def finddatastart(self, x, i):
        '''
        Find the start of settled data

        inputs:
                x = binned data
                i = the bin for settled data
        outputs:
                index = the starting index of settled data
        '''
        index = sum([len(j) for j in x[:i]])

        return index

    def ptest(self, x, alpha):
        '''
        Find the p-values for each bin with respect to the last bin

        inputs:
                x = binned data
                alpha = the significance level
        outputs:
                index = The last bin where the p-values is less than alpha
        '''

        pvals = [st.ttest_ind(i, x[-1], equal_var=False)[1] for i in x]

        count = 0
        for i in pvals:
            if i < alpha:
                index = count

            count += 1

        index += 1  # Skip the index that failed

        return index

    def slopeoverstd(self, x, m):
        '''
        Calcualte the slope of bins over their std

        inputs:
                x = binned data
                m = slope of binned data
                std = std of unbinned data
        outputs:
        '''

        deviations = [np.std(i) for i in x]
        divisions = [i/j for i, j in zip(m, deviations)]

        sigma = np.std(divisions)

        count = 0
        for i in divisions:
            if i > sigma:
                index = count

            count += 1

        index += 1  # Skip the index that failed

        return index

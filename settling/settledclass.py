from scipy import stats as st
from uncertainty.autocorrelation import autocorrelation

import pandas as pd
import numpy as np


def failfrequencycheck(onoff, alpha):
    '''
    Checks if the fail freequency of bins is above a threshold.

    input:
            onoff = the fail (1) and pass (0) list
            alpha = the probability criterion

    output:
            index = the choosen index that passes the test
    '''

    n = len(onoff)

    # Split fail indexes set for analysis
    if sum(onoff) == 0:
        index = 0

    else:
        rev = onoff[::-1]  # Reverse list to start from right

        # Indexes of failure
        failindexes = [i for i, x in enumerate(onoff) if x]

        # Indexes of failure in reversed list
        revfailindexes = sorted([n-i-1 for i in failindexes])

        # Gather ranges to evaluate frequency of failure
        revranges = []
        for i in revfailindexes:
            revranges.append(rev[:i])

        revranges.pop(0)  # The first will be empty or all zeros
        revranges.append(rev)  # Include all in case the last fails

        for i in revranges:

            # Check for first range that fails the frequency check
            if np.mean(i) > alpha:
                revindex = [j for j, x in enumerate(i) if x]
                revindex = max(revindex)
                index = n-revindex
                break

            else:
                index = 0

    return index


def ptest(x, nullhyp, a, alpha=0.05):
    '''
    Find the p-values for each bin with respect to the last bin.

    inputs:
            x = binned data
            nullhyp = null hypothesis
            a = the number of bins
            alpha = the significance level
    outputs:
            pvals = p-values for each bin with respect to the last bin
            index = last bin where the p-values is less than alpha
            alpha = return alpha if default is used
    '''

    # Store the bin where p-value is less than alpha
    onoff = list(np.zeros(a, dtype=int))

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

    index = failfrequencycheck(onoff, alpha)

    return pvals, index


class settled(object):
    '''
    Class to grab the indexes of settled data based on slopes per bin.
    Data has to be sufficiently long to not breack this code.
    '''

    def __init__(self, x, y, alpha=0.05):
        '''
        Devide data into a number of bins.

        inputs:
                x = x-axis data
                y = y-axis data
                alpha = the significance level
        '''

        self.x = x
        self.y = y
        self.n = len(x)  # Data length

        self.alpha = alpha  # Defined under ptest function
        self.binselect = {}  # Store selected settled bin bin
        self.indexes = {}  # Store first index of settled data
        self.warnings = {}  # Store warning messages

    def binsize(self):
        '''
        Use autocorrelation function to find correlation length.

        outputs:
                b = length of bins (approximate)
        '''

        k, r, index = autocorrelation(self.y)

        if index < 4:
            index = 4
            message = (
                       'Corrleation length is less than 4.' +
                       ' Setting correlation length to 4.'
                       )

            self.warnings['corrl'] = message

        self.b = index

        # Estimate the number of bins from block length
        self.a = self.n//self.b

        return self.a, self.b

    def batch(self):
        '''
        Devide data into a number of bins.

        outputs:
                self.xblocks = binned x-data
                self.yblocks = binned y-data
        '''

        self.xblocks = np.array_split(self.x, self.a)
        self.yblocks = np.array_split(self.y, self.a)

        return self.xblocks, self.yblocks

    def binslopes(self):
        '''
        Linear regression for each block of data.
        Data blocks must be same for both x and y.

        outputs:
                self.slopes = slopes for each bin
                self.errs = standard error in the slope for each bin
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

        self.binselect['slope change between bins'] = i

        return self.blockslopes, i

    def ptest(self):
        '''
        Find the p-values for each bin with respect to the last bin.

        outputs:
                distpvals = p-values for each bin with respect to the last bin
        '''

        distpvals, index = ptest(
                                 self.yblocks,
                                 self.yblocks[-1],
                                 self.a,
                                 self.alpha
                                 )

        keydistpvals = (
                        'bin distribution comparison to final bin ' +
                        r'($\alpha$=' +
                        str(self.alpha) +
                        ')'
                        )

        self.binselect[keydistpvals] = index
        self.distpvals = distpvals

        return distpvals

    def normaldistribution(self):
        '''
        Check whether a slope observation is outside the confidence interval
        of a normal distribution.

        outputs:
                ppf = values outside the limit given by the ppf
        '''

        interval = 1-self.alpha

        count = 0
        ppf = []
        onoff = []
        for i in self.blockslopes:
            # The minimum absolute value before going outside 2*sigma
            # The 2*sigma is defined by 1-alpha and can be altered
            limit = st.norm.ppf(interval, i, self.errs[count])
            ppf.append(limit)

            if (0.0 <= -limit) | (0.0 >= limit):
                onoff.append(1)
            else:
                onoff.append(0)

            count += 1

        index = failfrequencycheck(onoff, self.alpha)

        name = (
                r'mean slope within ' +
                str(100-100*self.alpha) +
                '% of zero slope'
                )

        self.binselect[name] = index
        self.ppf = ppf

        return ppf

    def finddatastart(self):
        '''
        Find the start of settled data.

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

    def warningsout(self):
        '''
        Return any warnings that come up.
        '''

        return self.warnings

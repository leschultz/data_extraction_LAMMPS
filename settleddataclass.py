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

        if a is None:
            a = n//b

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

        if x[1]-x[0] < 0.0:
            for i in range(0, n):
                if x[i+1]-x[i] > 0.0:
                    break

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

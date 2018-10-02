'''
Katzgraber, H. G. (2009). Introduction to Monte Carlo Methods.
Retrieved from http://arxiv.org/abs/0905.1629
'''

from matplotlib import pyplot as pl
from diffusionimport import load

import numpy as np
import os


class error(object):
    '''Compute the error of corelated data'''

    def __init__(self, data):
        '''Compute common factors for data'''

        self.data = data  # The data provided
        self.length = len(data)  # Length of data
        self.mean = np.mean(data)  # Mean of data

        # Mean of squared values of data
        self.meanofsquared = np.mean([i**2 for i in data])

    def correlationtime(self):
        '''
        Calculate the correlation time for correlated data.
        '''

        dl = 1  # Define how many points after to evaluate

        val = 0
        for i in range(0, self.length-dl):
            val += self.data[i]*self.data[i+dl]-self.mean**2

        val /= self.meanofsquared-self.mean**2  # The correlation time

        print(val)
        self.time = val

        return self.time

    def error(self):
        '''
        Calculate the error of a data set.
        '''

        val = (self.meanofsquared-self.mean**2)/(self.length-1)*(1+2*self.time)
        val **= 0.5

        self.error = val/(self.length)**0.5  # Standard Error

        return self.error

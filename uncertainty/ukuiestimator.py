'''
Error estimation based on Dr. Ryo Okui for correlated data.
The paper is below:
Asymptotically unbiased estimation of autocovariances and autocorrelations
for panel data with incidental trends

The Stack Exchange answer that helped is below:
https://stats.stackexchange.com/questions/274635/
calculating-error-of-mean-of-time-series

A paper that should be used to fix this script is as follows by H. Flyvbjerg
et al:
Error estimates on averages of correlated data

This script is NOT to be trusted for actuall error
'''

from uncertainty.autocovariance import autocovariance


def error(x):
    '''
    Calcualte the variance of the sample mean.

    inputs:
            x = correlated data
    outputs:
            SEM = standard error in the mean
    '''

    n = len(x)  # Length of data
    mean = sum(x)/n  # Mean of data

    gamma0 = autocovariance(x, 0, n, mean)  # 0-lag autocovariance

    gammaj = 0.0  # Variable for sum of k-lag autocovariances
    for j in range(1, n-1):
        gammaj += (n-j)/n*autocovariance(x, n, j, mean)

    gammaj *= 2.0

    variance = (gamma0+gammaj)/n
    sigma = variance**0.5
    SEM = sigma/n**0.5

    return SEM

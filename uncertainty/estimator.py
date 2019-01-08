'''
Error estimation based on a natural estimator for variance is applied.

The Stack Exchange answer that helped is below:
https://stats.stackexchange.com/questions/274635/
calculating-error-of-mean-of-time-series

A reference paper for error propagation is as follows:
Asymptotically unbiased estimation of autocovariances and autocorrelations
for panel data with incidental trends

The estimator used for error propagation is called a natural estimator.
This is the autocovariance. Other estimators can be used but this is the
simplest.
'''

from uncertainty.autocovariance import autocovariance


def error(x):
    '''
    Calcualte the variance of the sample mean.

    inputs:
            x = correlated data
    outputs:
            sigma = error by using a natural estimator for variance
    '''

    n = len(x)  # Length of data
    mean = sum(x)/n  # Mean of data

    # Use the natural estimator (not consitent)
    gamma0 = autocovariance(x, n, 0, mean)  # 0-lag autocovariance

    gammaj = 0.0  # Variable for sum of k-lag autocovariances

    # Note that the loop is for n and not n-1 because of how slicing works
    for j in range(1, n):
        gammaj += (n-j)*autocovariance(x, n, j, mean)

    gammaj *= 2.0/n  # Took division by n outside loop for efficiency

    variance = (gamma0+gammaj)/n
    sigma = variance**0.5

    return sigma

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


def autocovariance(x, k, n, mean):
    '''
    Find the autocovaraince between values k-lag appart.

    inputs:
            x = the set of data
            k = the lag between values
            n = the length of x data
            mean = the mean of x values
    outputs:
            gamma = the kth order autocovariance
    '''

    gamma = 0.0
    for i in range(0, n):
        for t in range(k, n):
            gamma += (x[t]-mean)*(x[t-k]-mean)

    gamma /= n*(n-k)

    return gamma


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
        # Break off higher covariances
        if j >= n**0.5:
            break
        gammaj += (n-j)/n*autocovariance(x, j, n, mean)

    gammaj *= 2.0

    variance = (gamma0+gammaj)/n
    sigma = variance**0.5
    SEM = sigma/n**0.5

    return SEM

def autocovariance(x, k, n, mean):

    gamma = 0.0
    for i in range(0, n):
        for t in range(k+1, n):
            gamma += (x[t]-mean)*(x[t-k]-mean)

    gamma /= n*(n-k)

    return gamma


def error(x, cut=None):
    n = len(x)
    mean = sum(x)/n

    gamma0 = autocovariance(x, 0, n, mean)

    gammaj = 0.0
    gammajchange = []
    jvals = []
    for j in range(0, n-1):
        if j == cut:
            break

        jvals.append(j)
        gammaj += (n-j)/n*autocovariance(x, j, n, mean)
        gammajchange.append(gammaj)

    gammaj *= 2.0

    variance = (gamma0+gammaj)/n  # Already devided by n for standard error
    sigma = variance**0.5

    return sigma, gamma0, gammajchange, jvals

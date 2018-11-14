def estimator(x, k, n, mean):

    gamma = 0.0
    for i in range(0, n-k):
        gamma += (x[i]-mean)*(x[i+k]-mean)

    gamma /= n

    return gamma


def error(x, last=None):
    n = len(x)
    mean = sum(x)/n
    minus = n-1

    gammak = 0.0
    gammakchange = []
    kvals = []
    for k in range(0, n-1):
        if k == last:
            break

        kvals.append(k)
        gammak += (n-k)/n*estimator(x, k, n, mean)
        gammakchange.append(gammak)

    gammak *= 2.0

    gamma0 = estimator(x, 0, n, mean)

    variance = gamma0+gammak
    sigma = variance**0.5
    error = sigma/(n**0.5)

    return error

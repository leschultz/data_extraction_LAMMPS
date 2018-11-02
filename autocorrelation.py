import numpy as np


def normautocor(x, k):

    n = len(x)
    mean = sum(x)/n

    valcor = 0.0
    for i in range(0, n-k):
        valcor += (x[i]-mean)*(x[i+k]-mean)

    valvar = 0.0
    for i in range(0, n):
        valvar += (x[i]-mean)**2.0

    rho = valcor/valvar

    return rho


def autocortime(x):

    n = len(x)

    tau = 0.0
    for i in range(0, n):
        tau += normautocor(x, i)

    tau *= 2.0
    tau += 1.0

    return tau


def error(x):
    n = len(x)

    tau = autocortime(x)
    error = tau
    error *= np.var(x)
    error /= n
    error **= 0.5

    return error, tau

import numpy as np


def autoerror(x):

    n = len(x)
    mean = sum(x)/n

    var = 0.0
    for i in range(0, n):
        for j in range(-i, n-i):
            cov = 0.0
            for k in range(0, n):
                cov += (x[i]-mean)*(x[i+j]-mean)

            cov /= n-1
            
            var += cov

    var /= n**2.0
    var **= 0.5  # return error

    return var


def autocorrelation(x, k):

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
        tau += autocorrelation(x, i)

    tau *= 2.0
    tau += 1

    return tau


def error(x):
    n = len(x)

    error = autocortime(x)
    error *= np.var(x)
    error /= n
    error **= 0.5

    return error

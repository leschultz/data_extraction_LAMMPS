def error(x, last=None):
    n = len(x)
    mean = sum(x)/n
    minus = n-1

    val = 0.0
    for i in range(0, n-1):
        if i == last:
            break

        cov = 0.0
        for j in range(0, n-1):
            cov += (x[i]-mean)*(x[i-j]-mean)
        cov /= minus

        val += (n-j)/n*cov

    val *= 2.0

    valvar = 0.0
    for i in range(0, n):
        valvar += x[i]**2.0

    valvar /= n
    valvar -= mean**2.0

    val += valvar
    val **= 0.5

    return val

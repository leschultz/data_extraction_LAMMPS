def autocovariance(x, k):
    n = len(x)
    mean = sum(x)/n
    minus = n-k

    val = 0.0
    for i in range(0, minus):
        val += (x[i]-mean)*(x[i+k]-mean)

    val /= minus

    return val


def autoerror(x):

    n = len(x)

    var = 0.0
    index = []
    values = []
    for i in range(0, n):
        for j in range(0-i, n-i):
            auto = autocovariance(x, j+i)

            var += auto
            values.append(auto)
            index.append(i+j)

    var /= n**2.0

    return var, index, values

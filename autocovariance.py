def rho(x, mean, n, k):
    numerator = 0.0
    for i in range(0, n-k):
        numerator += (x[i]-mean)*(x[i+k]-mean)

    denominator = 0.0
    for i in range(0, n):
        denominator += (x[i]-mean)**2.0

    normcor = numerator/denominator

    return normcor


def auto(x):
    n = len(x)
    mean = sum(x)/n

    k = []
    r = []
    for i in range(0, n):
        k.append(i)
        r.append(rho(x, mean, n, i))

    for i in k:
        if r[i] < 0.0:
            break
        else:
            last = i

    return k, r, last

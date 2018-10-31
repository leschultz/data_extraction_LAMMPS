import numpy as np


def covariance(x, y):
    n = len(x)
    meanx = sum(x)/n
    meany = sum(y)/n

    val = 0.0
    for i in range(0, n):
        val += (x[i]-meanx)*(y[i]-meany)

    val /= n-1

    return val


def errorchain(x, period):
    n = len(x)

    # Split data for equal distribution sections
    blocks = [x[i:i+period] for i in range(0, n, period)]

    # Check needed length for analysis for each block
    count = 0
    for block in blocks:
        if len(block) != period:
            index = count
        count += 1

    # Delete the shorter block
    del blocks[index]

    # Get the number of blocks
    nblocks = len(blocks)

    # Compute the covariance between blocks
    valcov = 0.0
    for i in range(0, nblocks):
        for j in range(0, nblocks):
            valcov += covariance(blocks[i], blocks[j])

    valcov /= nblocks

    # Compute variance of each block
    valvar = 0.0
    for i in range(0, nblocks):
        valvar += np.var(blocks[i])

    valvar /= nblocks

    variance = valvar+valcov
    error = variance**0.5

    return error

def other(x, period):
    n = len(x)

    # Split data for equal distribution sections
    blocks = [x[i:i+period] for i in range(0, n, period)]

    # Check needed length for analysis for each block
    count = 0
    for block in blocks:
        if len(block) != period:
            index = count
        count += 1

    # Delete the shorter block
    del blocks[index]

    # Get the number of blocks
    nblocks = len(blocks)

    valvar = np.var(x[0])

    valcor = 0.0
    for i in range(0, nblocks-1):
        valcor += (nblocks-i)/nblocks*covariance(blocks[0], blocks[0+i])
    valcor *= 2.0

    variance = valvar+valcor
    sigma = variance**0.5

    return sigma

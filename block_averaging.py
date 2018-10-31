def block(data, n=10):
    '''
    Devides the data into ten portions (default) to do block averaging.
    '''

    # Divide the data into blocks
    blocks = [data[i::n] for i in range(n)]

    # Average the blocks and find their error in the mean
    averages = [sum(i)/len(i) for i in blocks]
    mean = sum(averages)/n

    val = 0.0
    for i in range(0, n):
        val += (averages[i]-mean)**2.0

    val /= n

    sigma = val**0.5

    return mean, sigma

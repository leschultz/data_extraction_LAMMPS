'''http://www.eng.buffalo.edu/~kofke/ce530/Lectures/Lecture3/sld010.htm'''


def block(data, n=10):
    '''
    Devides the data into ten portions (default) to do block averaging.
    '''

    # Divide the data into blocks
    blocks = [data[i::n] for i in range(n)]

    # Average the blocks and find their error in the mean
    averages = [sum(i)/len(i) for i in blocks]
    n = len(averages)
    mean = sum(averages)/n

    # The standard deviation
    sigma = 0.0
    for i in range(0, n):
        sigma += averages[i]**2.0

    sigma /= n
    sigma -= mean**2.0
    sigma **= 0.5

    eim = sigma/(n)**0.5

    return mean, eim

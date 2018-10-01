from itertools import islice


def load(name, delimiter=' '):
    '''
    This function loads the diffusion data from multiple origins.
    '''

    # Save the headers from the data file
    with open(name) as file:
        for line in islice(file, 0, 1):
            header = line.strip().split(delimiter)

    # Crate a dictionary to store lists of values
    data = {}
    for head in header:
        data[head] = []

    # Save the data for diffusion
    with open(name) as file:
        next(file)
        for line in file:
            value = line.strip().split(delimiter)
            value = [float(i) for i in value]

            count = 0
            for item in value:
                data[header[count]].append(value[count])
                count += 1

    # Return all diffusivity data
    return data

from itertools import islice
import os

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


def loaddiffusions(maindir):
    folders = os.listdir(maindir)

    data = {}
    for folder in folders:
        data[folder] = {}

        filepath = maindir+folder+'/datacalculated/diffusion/'
        files = os.listdir(filepath)

        origins = [filepath+i for i in files if 'origin' in i]
        regular = [filepath+i for i in files if 'origin' not in i]

        data[folder]['origins'] = origins
        data[folder]['regular'] = regular

    order = []  # Save the order of imported data
    regular = {}  # Save the single diffusivity values
    multiple = {}  # Save for multiple origins

    for key in data:
        order.append(key)
        for item in data[key]:
            if 'origins' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-2]
                    temp = float(temp[:-1])
                    loaded = load(name)

                    if multiple.get(temp) is None:
                        multiple[temp] = {}

                    for i in loaded:
                        if multiple[temp].get(i) is None:
                            multiple[temp][i] = []

                        multiple[temp][i].append(loaded[i])

            if 'regular' in item:
                for name in data[key][item]:
                    temp = name.split('_')[-1]
                    temp = float(temp[:-1])
                    with open(name) as file:
                        for line in islice(file, 0, 1):
                            header = line.strip().split(' ')

                    with open(name) as file:
                        for line in islice(file, 1, None):
                            value = line.strip().split(' ')
                            value = [float(i) for i in value]

                    if regular.get(temp) is None:
                        regular[temp] = {}

                    count = 0
                    for head in header:
                        if regular[temp].get(head) is None:
                            regular[temp][head] = []
                        regular[temp][head].append(value[count])
                        count += 1

    return regular, multiple, order

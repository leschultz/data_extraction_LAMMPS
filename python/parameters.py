from itertools import islice as it


def parser(name, start):
    '''
    Gather the relevant portions of the lammpstrj file.

    Inputs
    ------
    name: The name of the lammpstrj file of interest.
    start: The parsing start for the file.

    Return
    ------
    Timestep, number of atoms, box dimensions.
    '''

    count = 0
    data = []
    with open(name) as handle:
        for line in it(handle, start, None):
            value = line.strip().split(' ')
            data.append(value)

            if value[0] == 'ITEM:':
                count += 1
            if count >= 4:
                break

    # Save relevant system properties
    out = {}
    out['step'] = int(data[1][0])
    out['atom'] = int(data[3][0])
    out['xmin'] = float(data[5][0])
    out['xmax'] = float(data[5][1])
    out['ymin'] = float(data[6][0])
    out['ymax'] = float(data[6][1])
    out['zmin'] = float(data[7][0])
    out['zmax'] = float(data[7][1])

    return out


def gather(name):
    '''
    Gather attributes like data acquisition frequency and timestep.

    Inputs
    ------
    name: The name of the lammpstrj file fo interest.

    Outputs
    -------
    rate: The data acquisition rate from the lammpstrj file
    '''

    first = parser(name, 0)

    second = parser(name, first['atom']+len(first)+1)

    rate = second['step'] - first['step']

    return rate

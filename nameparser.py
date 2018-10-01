from PyQt5 import QtGui  # Added to be able to import ovito


def parse(name):
    '''
    Grab values from filename.
    '''

    # Parameters from the naming convention
    value = name.split('_')
    system = value[0]
    side = value[1].split('-')[1]
    hold1 = int(value[2].split('-')[1])
    hold2 = int(value[3].split('-')[1])
    hold3 = int(value[4].split('-')[1])
    dumprate = int(value[6].split('-')[1])
    inittemp = int(value[7].split('K-')[0])
    finaltemp = int(value[7].split('K-')[1][:-1])

    timestep = ''
    ptimestep = value[5].split('-')[1]
    for letter in ptimestep:
        if letter == 'p':
            letter = '.'
        timestep += letter

    timestep = float(timestep)

    points = [hold1, hold1+hold2, hold1+hold2+hold3]

    return points, timestep, dumprate

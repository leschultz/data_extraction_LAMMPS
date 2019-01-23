'''
Script to parse the LAMMPS output file containing temperature, pressure, and
energies.
'''

import pandas as pd


def readdata(filepath):
    '''
    Open a file and parse per line.
    '''

    # Open the file
    with open(filepath) as file:
        for line in file:

            # Gather the headers for data
            headers = line.strip().split(' ')

            # Stop for the first set of headers
            if 'Step' in headers:
                break

    # Open file again
    data = []
    with open(filepath) as file:
        for line in file:
            values = line.strip().split(' ')
            values = [i for i in values if '' is not i]

            # Try to gather exported data
            try:
                if values:
                    values = [float(i) for i in values]
                    values[0] = int(values[0])
                    data.append(values)
            except Exception:
                pass

    # Save the exported data into a pandas dataframe
    df = pd.DataFrame(data, columns=headers)
    df = df.drop_duplicates('Step')
    df = df.reset_index(drop=True)

    return df


def atoms(name):
    '''
    Open a file and find the number of atoms.
    '''

    # Open the file
    with open(name) as file:
        for line in file:
            if 'atoms' in line:
                atoms = line.strip().split(' ')
                atoms = int(atoms[1])
                break

    return atoms

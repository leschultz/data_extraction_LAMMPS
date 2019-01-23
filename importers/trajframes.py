'''
Import the steps that are printed onto a trajectory file.
'''

import sys
import re


def trajectorysteps(name):

    steps = []
    with open(name) as file:
        for line in file:
            if 'TIMESTEP' in line:
                line = next(file)
                line = int(line.strip('\n'))
                steps.append(line)

    return steps

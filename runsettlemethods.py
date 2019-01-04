'''
This script runs settled data analysis tools to determine if data is reliable.
This requires runsteps data exported.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
import argparse

from settledanalysis import run as setmeth

from infoparser import parameters

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', help='Input File for Settling Analysis')
parser.add_argument('-i', help='LAMMPS Runs Directory')
parser.add_argument('-o', help='Analysis Output Directory')
args = parser.parse_args()

# Parse the input file for settling analysis
with open(args.p) as file:
    for line in file:
        values = line.strip().split(' ')
        if 'alpha' in values[0]:
            alpha = float(values[0].split('=')[-1])

        if 'n0' in values[0]:
            n0 = int(values[0].split('=')[-1])

# Gather ditionary containing all the needed parameters for runs
runs = parameters(args.i)
runs.files()
param = runs.inputinfo()

setmeth(param, args.o, alpha, n0)  # Settling analysis

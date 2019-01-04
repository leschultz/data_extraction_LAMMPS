'''
This script runs all the possible analysis tools developed
'''

from PyQt5 import QtGui  # Added to be able to import ovito
import argparse

from settledanalysis import run as setmeth
from stepanalysis import run as stepmeth
from errormethods import run as errmeth

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

stepmeth(param, args.o)  # Use ovito for calculating diffuison and RDF
errmeth(args.o)  # Error Propagation
setmeth(param, args.o, alpha, n0)  # Settling analysis

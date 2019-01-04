'''
This script caluclates diffusion and RDF using Ovito.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
from infoparser import parameters
import argparse
import os

from stepanalysis import run as stepmeth

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='LAMMPS Runs Directory')
parser.add_argument('-o', help='Analysis Output Directory')
args = parser.parse_args()

# Gather ditionary containing all the needed parameters for runs
runs = parameters(args.i)
runs.files()
param = runs.inputinfo()

stepmeth(param, args.o)  # Use ovito for calculating diffuison and RDF

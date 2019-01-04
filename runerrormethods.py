'''
This script runs the error propagation methods. It needs the data exported by
runsteps.py.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
import argparse

from errormethods import run as errmeth

from infoparser import parameters

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Analysis Output Directory')
args = parser.parse_args()

errmeth(args.o)   # Error Propagation

'''
This script caluclates diffusion and RDF using Ovito.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
from importers.infoparser import parameters

import argparse
import logging
import shutil
import os

from physical.stepanalysis import run as stepmeth

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='LAMMPS Runs Directory')
parser.add_argument('-o', help='Analysis Output Directory')
parser.add_argument('-p', help='Input File for Settling Analysis')
args = parser.parse_args()

# Parse the input file for settling analysis
with open(args.p) as file:
    for line in file:
        values = line.strip().split(' ')
        if 'alpha' in values[0]:
            alpha = float(values[0].split('=')[-1])

# Create export directory
if not os.path.exists(args.o):
    os.makedirs(args.o)

# Setup a logging file
formating =(
            '%(asctime)s - ' +
            '%(name)s - ' +
            '%(levelname)s - ' +
            '%(message)s'
            )

logging.basicConfig(
                    filename=args.o+'/overview.log',
                    format=formating
                    )

# Gather ditionary containing all the needed parameters for runs
runs = parameters(args.i)
runs.files()
param = runs.inputinfo()

stepmeth(param, args.o, alpha)  # Use ovito for calculating diffuison and RDF

# Zip the original data and include in export directory
print('Compressing original data')
shutil.make_archive(args.o+'/originaldata', 'zip', base_dir=args.i)

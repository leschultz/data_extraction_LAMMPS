from PyQt5 import QtGui  # Added to be able to import ovito
from infoparser import parameters
import argparse
import os

from stepanalysis import run as stepmeth

parser = argparse.ArgumentParser()
parser.add_argument('-i')
parser.add_argument('-o')

args = parser.parse_args()

runs = parameters(args.i)
runs.files()
param = runs.inputinfo()

stepmeth(param, args.o)

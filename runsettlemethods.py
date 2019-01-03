from PyQt5 import QtGui  # Added to be able to import ovito
import argparse

from settledanalysis import run as setmeth

from infoparser import parameters

parser = argparse.ArgumentParser()
parser.add_argument('-p')
parser.add_argument('-i')
parser.add_argument('-o')

args = parser.parse_args()

with open(args.p) as file:
    for line in file:
        values = line.strip().split(' ')
        if 'alpha' in values[0]:
            alpha = float(values[0].split('=')[-1])

        if 'n0' in values[0]:
            n0 = int(values[0].split('=')[-1])

runs = parameters(args.i)
runs.files()
param = runs.inputinfo()

setmeth(param, args.o, alpha, n0)

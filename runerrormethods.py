from PyQt5 import QtGui  # Added to be able to import ovito
import argparse

from errormethods import run as errmeth

from infoparser import parameters

parser = argparse.ArgumentParser()
parser.add_argument('-p')
parser.add_argument('-i')
parser.add_argument('-o')

args = parser.parse_args()

if args.p:
    with open(args.p) as file:
        for line in file:
            values = line.strip().split(' ')
            if 'alpha' in values[0]:
                alpha = float(values[0].split('=')[-1])

            if 'n0' in values[0]:
                n0 = int(values[0].split('=')[-1])

errmeth(args.o)

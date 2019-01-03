from PyQt5 import QtGui  # Added to be able to import ovito
from infoparser import parameters
from single import analize

from errormethods import run as errmeth
from settledanalysis import run as setmeth

import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-p')
parser.add_argument('-i')
parser.add_argument('-o')

args = parser.parse_args()


def start(datadir):
    runs = parameters(datadir)
    runs.files()
    param = runs.inputinfo()

    return param


def run(param, exportdir):
    for item in param:
        filename = item

        printname = 'Gathering Data from File: '+filename

        print('-'*len(printname))
        print(printname)
        print('-'*len(printname))

        n = param[item]['iterations']
        increment = param[item]['increment']
        deltatemp = param[item]['deltatemp']
        starttemp = param[item]['tempstart']
        timestep = param[item]['timestep']
        dumprate = param[item]['dumprate']

        hold2 = param[item]['hold2']
        hold3 = param[item]['hold3']

        savepath = exportdir+'/'+item.split('/')[-2]

        for iteration in list(range(0, n)):

            print(
                  'Temperature step: ' +
                  str(starttemp-iteration*deltatemp) +
                  ' [K]'
                  )

            hold1 = param[item]['hold1']
            hold1 += iteration*increment

            points = [hold1, hold1+hold2, hold1+hold2+hold3]

            # Do averaging for files
            value = analize(
                            item,
                            savepath,
                            points[1],
                            points[2],
                            timestep,
                            dumprate,
                            [points[0], points[1], points[2]],
                            10,
                            50
                            )

            value.calculate_time()
            value.calculate_msd()
            value.calculate_rdf()
            value.calculate_diffusion()
            value.multiple_origins_diffusion()
            data = value.calculation_export()

            savename = (
                        item.split('/')[-2] +
                        '_' +
                        str(starttemp-iteration*deltatemp).split('.')[0] +
                        'K'
                        )

            value.plot_msd(savename)
            value.plot_diffusion(savename)
            value.plot_rdf(savename)
            value.save_msd(savename)
            value.save_rdf(savename)
            value.save_multiple_origins_diffusion(savename)
            value.save_diffusion(savename)


if args.p:
    with open(args.p) as file:
        for line in file:
            values = line.strip().split(' ')
            if values[0] != '#':
                print(values)

param = start(args.i)
run(param, args.o)
errmeth(args.o)
setmeth(param, args.o)

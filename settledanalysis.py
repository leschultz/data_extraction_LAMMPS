from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import colors as mcolors
from matplotlib import pyplot as pl
from cycler import cycler

from infoparser import parameters
from outimport import readdata
from settleddataclass import settled

import numpy as np
import os

colors = list(mcolors.BASE_COLORS.keys())
colors = [i for i in colors if i != 'r']


def run(param, savepath):
    for item in param:

        path = item.replace('uwtraj.lammpstrj', '')
        outfile = path+'test.out'
        printname = 'Settling Methods for Run: '+outfile

        folder = '/'+path.split('/')[-2]

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

        df = readdata(outfile)

        time = [timestep*i for i in df['Step']]
        df['time'] = time

        for iteration in list(range(0, n)):

            expectedtemp = starttemp-iteration*deltatemp

            print(
                  'Temperature step: ' +
                  str(expectedtemp) +
                  ' [K]'
                  )

            savename = (
                        item.split('/')[-2] +
                        '_' +
                        str(starttemp-iteration*deltatemp).split('.')[0] +
                        'K'
                        )

            hold1 = param[item]['hold1']
            hold1 += iteration*increment

            points = [hold1, hold1+hold2, hold1+hold2+hold3]

            dataindexes = df['Step'].between(points[1], points[2])

            time = list(df['time'][dataindexes])
            temp = list(df['Temp'][dataindexes])

            setindexes = settled(time, temp)
            index = setindexes.binsize()
            binnedtime, binnedtemp = setindexes.batch()

            setindexes.binslopes()

            setindexes.binnedslopetest()
            setindexes.slopetest(expectedtemp)

            fitvals = setindexes.ptestfit(expectedtemp)

            txtname = (
                       savepath+folder +
                       '/datacalculated/settling/temperature_' +
                       savename +
                       '.txt'
                       )

            dfout = setindexes.returndata()
            dfout.to_csv(txtname, sep=' ', index=False)

            slopeerr = fitvals[0]
            averages = fitvals[1]
            slopeerrbin = fitvals[2]
            start = fitvals[3]
            slopestart = fitvals[4]

            indexes = setindexes.finddatastart()

            fig, ax = pl.subplots()

            ax.plot(
                    time,
                    temp,
                    linestyle='none',
                    color='r',
                    marker='.',
                    label='Data'
                    )

            count = 0
            for key in indexes:
                try:
                    ax.axvline(
                               x=time[indexes[key]],
                               linestyle='--',
                               color=colors[count],
                               label='Method: '+key
                               )

                except Exception:
                    pass

                count += 1

            ax.set_xlabel('Time [ps]')
            ax.set_ylabel('Temperature [K]')
            ax.grid()
            ax.legend(loc='best')
            fig.tight_layout()
            fig.savefig(
                        savepath +
                        folder +
                        '/images/settling/temperature_' +
                        savename
                        )

            pl.close('all')

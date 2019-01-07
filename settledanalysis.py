from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import colors as mcolors
from matplotlib import pyplot as pl

from outimport import readdata
from settleddataclass import settled

colors = list(mcolors.BASE_COLORS.keys())
colors = [i for i in colors if i != 'r']
lstyle = ['-.', '--', ':']


def methodplotter(time, ax, indexes):
    '''
    Plot a vertial line at an index determined by settling methods.

    inputs:
            ax = the plot to apply vertical lines
            time = time data of run
            indexes = a dictionary containing the method name and the settled
                      index
    '''

    count = 0
    for key in indexes:
        try:
            ax.axvline(
                       x=time[indexes[key]],
                       linestyle=lstyle[count],
                       color=colors[count],
                       label='Method: '+key
                       )

        except Exception:
            ax.axvline(
                       x=time[-1],
                       linestyle=lstyle[count],
                       color=colors[count],
                       label='Method: '+key+' unsettled'
                       )

        count += 1



def run(param, savepath, alpha, n0):
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

            # Run for temperature data
            temp = list(df['Temp'][dataindexes])

            setindexes = settled(time, temp, alpha)
            index = setindexes.binsize()
            binnedtime, binnedtemp = setindexes.batch()

            setindexes.binslopes()
            setindexes.binnedslopetest()
            setindexes.ptest()
            setindexes.normaldistribution()

            txtname = (
                       savepath+folder +
                       '/datacalculated/settling/temperature_' +
                       savename +
                       '.txt'
                       )

            dfout = setindexes.returndata()
            dfout.to_csv(txtname, sep=' ', index=False)

            indexes = setindexes.finddatastart()

            fig, ax = pl.subplots()

            ax.plot(
                    time,
                    temp,
                    linestyle='none',
                    color='r',
                    marker='.',
                    label=(
                           'Data (start of hold is ' +
                           str(points[1]*timestep) +
                           ' [ps])'
                           )
                    )

            methodplotter(time, ax, indexes)

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

            # Run for pressures
            press = list(df['Press'][dataindexes])

            setindexes = settled(time, press, alpha)
            index = setindexes.binsize()
            binnedtime, binnedtemp = setindexes.batch()

            setindexes.binslopes()
            setindexes.binnedslopetest()
            setindexes.ptest()
            setindexes.normaldistribution()

            txtname = (
                       savepath+folder +
                       '/datacalculated/settling/pressure_' +
                       savename +
                       '.txt'
                       )

            dfout = setindexes.returndata()
            dfout.to_csv(txtname, sep=' ', index=False)

            indexes = setindexes.finddatastart()

            fig, ax = pl.subplots()

            ax.plot(
                    time,
                    press,
                    linestyle='none',
                    color='r',
                    marker='.',
                    label=(
                           'Data (start of hold is ' +
                           str(points[1]*timestep) +
                           ' [ps])'
                           )
                    )

            methodplotter(time, ax, indexes)

            ax.set_xlabel('Time [ps]')
            ax.set_ylabel('Pressure [bars]')
            ax.grid()
            ax.legend(loc='best')
            fig.tight_layout()
            fig.savefig(
                        savepath +
                        folder +
                        '/images/settling/pressure_' +
                        savename
                        )

            pl.close('all')

from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import colors as mcolors
from matplotlib import pyplot as pl

from settling.settledclass import settled
from importers.outimport import readdata

# Add colors and line stiles for three methods
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

        # Failure means that the index is beyond range
        except Exception:
            ax.axvline(
                       x=time[-1],
                       linestyle=lstyle[count],
                       color=colors[count],
                       label='Method: '+key+' UNSETTLED'
                       )

        count += 1


def run(param, savepath, alpha):
    '''
    Run settling methods for all runs in a directory.
    '''

    # Apply for each run in the main directory
    for item in param:

        path = item.replace('uwtraj.lammpstrj', '')  # Run directory
        outfile = path+'test.out'  # LAMMPS data export
        printname = 'Settling Methods for Run: '+outfile

        folder = '/'+path.split('/')[-2]  # Run name

        # Print on screen the run analyzed
        print('-'*len(printname))
        print(printname)
        print('-'*len(printname))

        # Parsed parameters
        n = param[item]['iterations']
        increment = param[item]['increment']
        deltatemp = param[item]['deltatemp']
        starttemp = param[item]['tempstart']
        timestep = param[item]['timestep']
        dumprate = param[item]['dumprate']
        hold2 = param[item]['hold2']
        hold3 = param[item]['hold3']

        # Parsed data exported from LAMMPS
        df = readdata(outfile)

        time = [timestep*i for i in df['Step']]  # Convert setps to time
        df['time'] = time  # Add time to df

        # Apply settle analysis on each step of run
        for iteration in list(range(0, n)):

            # Temperature defined by LAMMPS input file
            expectedtemp = starttemp-iteration*deltatemp

            print(
                  'Temperature step: ' +
                  str(expectedtemp) +
                  ' [K]'
                  )

            # Savename convention
            savename = (
                        item.split('/')[-2] +
                        '_' +
                        str(starttemp-iteration*deltatemp).split('.')[0] +
                        'K'
                        )

            # Find the start of quench to the next step
            hold1 = param[item]['hold1']
            hold1 += iteration*increment

            # Start of quench, start of hold, and end of hold
            points = [hold1, hold1+hold2, hold1+hold2+hold3]

            # Data in hold range
            dataindexes = df['Step'].between(points[1], points[2])

            time = list(df['time'][dataindexes])

            # Run for temperature data
            temp = list(df['Temp'][dataindexes])

            # Apply methods in settleddataclass.py
            setindexes = settled(time, temp, alpha)
            setindexes.binsize()
            setindexes.batch()
            setindexes.binslopes()
            setindexes.binnedslopetest()
            setindexes.ptest()
            setindexes.normaldistribution()

            # Naming convention for temperature data from settling
            txtname = (
                       savepath+folder +
                       '/datacalculated/settling/temperature_' +
                       savename +
                       '.txt'
                       )

            # Export a text file
            dfout = setindexes.returndata()
            dfout.to_csv(txtname, sep=' ', index=False)

            # The indexes of data from settling methods
            indexes = setindexes.finddatastart()

            # Plot temperature step along with method limits
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

            # Apply methods in settleddataclass.py
            setindexes = settled(time, press, alpha)
            setindexes.binsize()
            setindexes.batch()
            setindexes.binslopes()
            setindexes.binnedslopetest()
            setindexes.ptest()
            setindexes.normaldistribution()

            # Naming convention for temperature data from settling
            txtname = (
                       savepath+folder +
                       '/datacalculated/settling/pressure_' +
                       savename +
                       '.txt'
                       )

            # Export a text file
            dfout = setindexes.returndata()
            dfout.to_csv(txtname, sep=' ', index=False)

            # The indexes of data from settling methods
            indexes = setindexes.finddatastart()

            # Plot temperature step along with method limits
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

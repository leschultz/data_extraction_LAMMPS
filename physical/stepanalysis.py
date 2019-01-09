'''
Apply the diffusion and RDF analysis for all steps in a run.
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import colors as mcolors
from matplotlib import pyplot as pl

from settling.settledclass import settled
from importers.outimport import readdata
from physical.singlestep import analize

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


def run(param, exportdir, alpha):
    '''
    Iterate initial data analysis for all steps in all runs
    '''

    # Apply for each run in the main directory
    for item in param:

        path = item.replace('uwtraj.lammpstrj', '')  # Run directory
        folder = '/'+path.split('/')[-2]  # Run name
        outfile = path+'test.out'  # LAMMPS data export

        printname = 'Gathering Data from File: '+item

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

        # The path to save in
        savepath = exportdir+'/'+item.split('/')[-2]

        # Apply settle analysis on each step of run
        for iteration in list(range(0, n)):

            # Temperature defined by LAMMPS input file
            tempstr = str(int(starttemp-iteration*deltatemp))

            print(
                  'Temperature step: ' +
                  tempstr +
                  ' [K]'
                  )

            # Savename convention
            savename = folder[1:]+'_'+tempstr+'K'

            # Naming convention for temperature settling data
            settlingtxt = (
                           savepath +
                           '/datacalculated/settling/temperature_' +
                           savename +
                           '.txt'
                           )

            # Naming convention for temperature settling image
            settlingimg = (
                           savepath + 
                           '/images/settling/temperature_' +
                           savename
                           )

            # Find the start of quench to the next step
            hold1 = param[item]['hold1']
            hold1 += iteration*increment

            # Start of quench, start of hold, and end of hold
            points = [hold1, hold1+hold2, hold1+hold2+hold3]

            # Data in hold range
            dataindexes = df['Step'].between(points[1], points[2])

            time = list(df['time'][dataindexes])

            # Check when temperature settles
            temp = list(df['Temp'][dataindexes])

            # Apply methods in settleddataclass.py
            setindexes = settled(time, temp, alpha)
            setindexes.binsize()
            setindexes.batch()
            setindexes.binslopes()
            setindexes.binnedslopetest()
            setindexes.ptest()
            setindexes.normaldistribution()

            # The indexes of data from settling methods
            indexes = setindexes.finddatastart()

            # Start the method for data analysis for the step
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

            value.calculate_time()  # Time normalized
            value.calculate_msd()  # Mean Squared Displacement
            value.calculate_rdf()  # Radial Distribution Function
            value.calculate_diffusion()  # Diffusion from linear fit
            value.multiple_origins_diffusion()  # Diffusion Multiple Origins
            data = value.calculation_export()  # Grab data calculated

            # Plot relevant plots
            value.plot_msd(savename)
            value.plot_diffusion(savename)
            value.plot_rdf(savename)

            # Save relevant data
            value.save_msd(savename)
            value.save_rdf(savename)
            value.save_multiple_origins_diffusion(savename)
            value.save_diffusion(savename)

            # Export a text file for settling analysis data
            dfout = setindexes.returndata()
            dfout.to_csv(settlingtxt, sep=' ', index=False)

            # Plot temperature step along with method limits for settling
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
            fig.savefig(settlingimg)

            pl.close('all')

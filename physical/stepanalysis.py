'''
Apply the diffusion and RDF analysis for all steps in a run.
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import colors as mcolors
from matplotlib import pyplot as pl
from scipy import stats as st

import pandas as pd
import numpy as np

from uncertainty.batchmeans import error as batch
from uncertainty.estimator import error as okui

from uncertainty.autocorrelation import autocorrelation

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

        # Apply analysis on each step of run
        differrors = []
        differrorspercent = []
        for iteration in range(n):

            # Temperature defined by LAMMPS input file
            holdtemp = starttemp-iteration*deltatemp
            tempstr = str(int(holdtemp))

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

            # The indexes of data from settling methods
            indexes = setindexes.finddatastart()

            # Get the maximum cut
            cuts = []
            for key in indexes:
                cuts.append(indexes[key])

            cut = max(cuts)  # The cut index
            cut *= dumprate  # Convert to MD steps

            # Start the method for data analysis for the step
            value = analize(
                            item,
                            savepath,
                            points[1]+cut,
                            points[2],
                            timestep,
                            dumprate,
                            [points[1], points[2]],
                            10,
                            20
                            )

            value.calculate_time()  # Time normalized
            value.calculate_msd()  # Mean Squared Displacement
            value.calculate_rdf()  # Radial Distribution Function
            value.calculate_diffusion()  # Diffusion from linear fit
            value.multiple_origins_diffusion()  # Diffusion Multiple Origins
            data = value.calculation_export()  # Grab data calculated

            elements = list(data.diffmulti.keys())
            elements = [i for i in elements if '_' not in i]

            for key in elements:

                # Autocorrelation function
                k, r, corl = autocorrelation(data.diffmulti[key])

                # If the correlation length is zero, give at least some data
                if corl < 4:
                    corl = 4

                # Name for autocorrelation plot
                acorname = (
                            savepath +
                            '/images' +
                            '/errormethods' +
                            '/autocorrelation' +
                            '/autocorrelation_' +
                            savename +
                            '_element_' +
                            key
                            )

                # Plot autocorrelation function for each element
                pl.plot(k, r, 'b.', label=tempstr+' [K]')
                pl.axvline(
                        x=corl,
                        linestyle='--',
                        color='r',
                        label='Correlation Length='+str(corl)
                        )

                pl.grid()
                pl.xlabel('k-lag [index]')
                pl.ylabel('Autocorrelation [-]')
                pl.legend(loc='upper right')
                pl.tight_layout()
                pl.savefig(acorname)
                pl.clf()

                errdf = {}
                errdfpercent = {}
                modata = list(data.diffmulti[key])  # multiple origins

                # Apply uncertainty propagation methods
                okuierr = okui(modata)
                batch5 = batch(modata, a=5)[0]
                batch10 = batch(modata, a=10)[0]
                batchcorl = batch(modata, b=corl)[0]
                scipyerr = st.sem(modata)

                # Percent Errors
                conversion = 100/data.diffusion[key]
                perokuierr = okuierr*conversion
                perbatch5 = batch5*conversion
                perbatch10 = batch10*conversion
                perbatchcorl = batchcorl*conversion
                perscipyerr = scipyerr*conversion

                methods = [
                           'Natural Estimator',
                           'Batch Means 5 Blocks',
                           'Batch Means 10 Blocks',
                           'Batch Means Correlation Length Blocks',
                           'Standard Error in the Mean'
                           ]

                # Save to dictionary that will be use in a data frame
                errdf[methods[0]] = okuierr
                errdf[methods[1]] = batch5
                errdf[methods[2]] = batch10
                errdf[methods[3]] = batchcorl
                errdf[methods[4]] = scipyerr

                # Percent Errors
                errdfpercent[methods[0]] = perokuierr
                errdfpercent[methods[1]] = perbatch5
                errdfpercent[methods[2]] = perbatch10
                errdfpercent[methods[3]] = perbatchcorl
                errdfpercent[methods[4]] = perscipyerr

                errdf['holdtemp'] = holdtemp  # Hold temperature
                errdf['element'] = key  # Element

                errdfpercent['holdtemp'] = holdtemp  # Hold temperature
                errdfpercent['element'] = key  # Element

                differrors.append(errdf)
                differrorspercent.append(errdfpercent)

            # Save relevant data
            value.save_msd(savename)
            value.save_rdf(savename)
            value.save_multiple_origins_diffusion(savename)
            value.save_diffusion(savename)

            # Plot relevant plots
            value.plot_msd(savename)
            value.plot_diffusion(savename)
            value.plot_rdf(savename)

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

        # Make a dataframe containing uncertainties for a run
        dferrs = pd.DataFrame(differrors)
        errtxt = (
                  savepath +
                  '/datacalculated/errormethods/uncertainties.txt'
                  )

        dferrs.to_csv(errtxt, sep=' ', index=False)

        dferrspercent = pd.DataFrame(differrorspercent)
        errtxtpercent = (
                         savepath +
                         '/datacalculated/' +
                         'errormethods/percentuncertainties.txt'
                         )

        dferrspercent.to_csv(errtxtpercent, sep=' ', index=False)

        elements = set(list(dferrs.element))

        # Save name for multiple origin uncertaintites
        errname = (
                   savepath +
                   '/images/errormethods/errors/' +
                   'mo_' +
                   '_element_'
                   )

        # Start the error plots
        for key in elements:
            condition = dferrs.element == key
            conditionper = dferrspercent.element == key

            ax = dferrs[condition].plot(x='holdtemp', style='.')

            ax.set_xlabel('Temperature [K]')
            ax.set_ylabel('Diffusion MO Error [*10^-4 cm^2 s^-1]')
            ax.grid()

            plot = ax.get_figure()
            plot.tight_layout()
            plot.savefig(errname+key)

            axper = dferrspercent[conditionper].plot(x='holdtemp', style='.')

            axper.set_xlabel('Temperature [K]')
            axper.set_ylabel('Diffusion MO Percent Error')
            axper.grid()

            plotper = axper.get_figure()
            plotper.tight_layout()
            plotper.savefig(errname+key+'_percent')

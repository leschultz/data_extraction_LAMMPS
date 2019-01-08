from matplotlib import pyplot as pl
from scipy import stats as st
from matplotlib import lines

import pandas as pd
import numpy as np
import math

from uncertainty.ukuiestimator import error as ukui
from uncertainty.batchmeans import error as batch

from uncertainty.autocorrelation import autocorrelation
from importers.dfdiff import diffusionimport


def percent(x, y):
    '''
    Return a percent value.

    inputs:
            x = uncertainty values
            y = absolute values
    output:
            z = list of percent uncertainties
    '''

    z = [i/j*100.0 for i, j in zip(x, y)]

    return z


def run(datadir):
    '''
    Run uncerainty analysis for all runs in a directory.
    '''

    # Apply for each run in the main directory
    data = diffusionimport(datadir)
    errors = {}
    for folder in data:

        # Run name
        printname = 'Error Analysis on Run: '+datadir+folder

        # Print on screen the run analyzed
        print('-'*len(printname))
        print(printname)
        print('-'*len(printname))

        # Apply uncertainty methods for each step
        errors[folder] = []
        for temp in data[folder]['origins']:

            tempstr = str(math.ceil(temp))  # Step temperature

            print('Temperature step: '+tempstr+' [K]')

            # Diffusion coluns for all and each element
            cols = list(data[folder]['origins'][temp].columns.values)[1:]
            cols = [i for i in cols if 'err' not in i]

            # Single linear regression diffusion
            regulardata = data[folder]['regular'][temp]

            # Multiple origins data for diffusion
            modata = data[folder]['origins'][temp]

            # Apply error methods for all and each element
            errordf = {}
            for col in cols:

                # Autocorrelation function
                k, r, index = autocorrelation(modata[col])

                # Name for autocorrelation plot
                name = (datadir +
                        '/' +
                        folder +
                        '/images' +
                        '/errormethods' +
                        '/autocorrelation' +
                        '/autocorrelation_temp_' +
                        tempstr +
                        '_' +
                        col
                        )

                pl.plot(k, r, 'b.', label=tempstr+' [K]')
                pl.axvline(
                        x=index,
                        linestyle='--',
                        color='r',
                        label='Correlation Length='+str(index)
                        )
                pl.grid()
                pl.xlabel('k-lag [index]')
                pl.ylabel('Autocorrelation [-]')
                pl.legend(loc='upper right')
                pl.tight_layout()
                pl.savefig(name)
                pl.clf()

                # Apply error methods
                errordf[col+'_diff'] = regulardata[col]
                errordf[col+'_fiterr'] = regulardata[col+'_err']
                errordf[col+'_mo_ukui'] = ukui(list(modata[col]))
                errordf[col+'_mo_batch(a=5)'] = batch(
                                                      list(modata[col]),
                                                      a=5
                                                      )[0]

                errordf[col+'_mo_batch(a=10)'] = batch(
                                                       list(modata[col]),
                                                       a=10
                                                       )[0]

                corbatch = batch(list(modata[col]), b=k[index])
                errordf[col+'_mo_batch(a=corbatch)'] = corbatch[0]
                errordf[col+'_mo_scipysem'] = st.sem(list(modata[col]))

                errordf['temp'] = temp
                errordf = pd.DataFrame(errordf, index=[0])
                errors[folder].append(errordf)

    # Plot data from error methods error methods
    for folder in data:
        errors[folder] = pd.concat(errors[folder])
        exportname = (
                      datadir +
                      '/' +
                      folder +
                      '/datacalculated/errormethods/correrrs.txt'
                      )

        errors[folder].to_csv(
                                exportname,
                                sep=' ',
                                index=False
                                )

    # Plotting style for batch means with 5 bins
    batch5label = lines.Line2D(
                            [],
                            [],
                            color='b',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (a=5)'
                            )

    # Plotting style for batch means with 10 bins
    batch10label = lines.Line2D(
                            [],
                            [],
                            color='r',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (a=10)'
                            )

    # Plotting style for batch means with bin length of one correlation length
    batchlcorrlabel = lines.Line2D(
                            [],
                            [],
                            color='g',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (b=lcorr)'
                            )

    # Plotting style for a method in a paper by Ukoi
    ukuilabel = lines.Line2D(
                            [],
                            [],
                            color='y',
                            marker='+',
                            linestyle='None',
                            markersize=8,
                            label='Ukui Estimator'
                            )

    # Plotting style for data treated as independent
    scipylabel = lines.Line2D(
                            [],
                            [],
                            color='k',
                            marker='x',
                            linestyle='None',
                            markersize=8,
                            label='Scipy SEM'
                            )

    # List containing each of the plotting styles
    plotlabels = []
    plotlabels.append(batch5label)
    plotlabels.append(batch10label)
    plotlabels.append(batchlcorrlabel)
    plotlabels.append(ukuilabel)
    plotlabels.append(scipylabel)

    size = (15, 5)  # Define figure size

    # Plotting caluclated errors
    for folder in errors:

        # Gather the elements including all
        cols = list(errors[folder].columns.values)
        elements = [i.split('_')[0] for i in cols if len(i.split('_')) > 1]
        elements = list(set(elements))

        # Plot errors for each element including all
        for el in elements:

            # Start plotting diffusions and their fit errors per temperature
            # From a single linear interpolation
            fig, ax = pl.subplots(1, 2, figsize=size)

            x = errors[folder]['temp']  # Step temperature

            # Plot diffusion for each temperature
            ax[0].plot(x, errors[folder][el+'_diff'], 'b.')
            ax[0].set_ylabel('Diffusion [*10^-4 cm^2 s^-1]')
            ax[0].set_xlabel('Temperature [K]')
            ax[0].grid()

            # Plot standard error in the slope from fitting
            ax[1].plot(x, errors[folder][el+'_fiterr'], 'r.')
            ax[1].set_ylabel('Diffusion Fit Error [*10^-4 cm^2 s^-1]')
            ax[1].set_xlabel('Temperature [K]')
            ax[1].grid()

            # Save name for diffusion and fit error plots
            name = (datadir +
                    '/' +
                    folder +
                    '/images/errormethods/errors/' +
                    'element_' +
                    el
                    )

            fig.tight_layout()
            fig.savefig(name)
            pl.close(fig)

            # Start plotting all other error methods
            fig, ax = pl.subplots(1, 2, figsize=size)

            # Absolute uncertainties from multiple origins on diffusion
            ax[0].plot(x, errors[folder][el+'_mo_batch(a=5)'], 'b.')
            ax[0].plot(x, errors[folder][el+'_mo_batch(a=10)'], 'r.')
            ax[0].plot(x, errors[folder][el+'_mo_batch(a=corbatch)'], 'g.')
            ax[0].plot(x, errors[folder][el+'_mo_ukui'], 'y+')
            ax[0].plot(x, errors[folder][el+'_mo_scipysem'], 'kx')

            ax[0].set_ylabel('Diffusion MO Error [*10^-4 cm^2 s^-1]')
            ax[0].set_xlabel('Temperature [K]')
            ax[0].legend(handles=plotlabels, loc='upper left')
            ax[0].grid()

            # Change values to percent error
            diff = errors[folder][el+'_diff']

            runsbatch5percent = percent(
                                    errors[folder][el+'_mo_batch(a=5)'],
                                    diff
                                    )

            runsbatch10percent = percent(
                                    errors[folder][el+'_mo_batch(a=10)'],
                                    diff
                                    )

            runsbatchlcorrpercent = percent(
                                            errors[folder][
                                                    el +
                                                    '_mo_batch(a=corbatch)'
                                                    ],
                                            diff
                                            )

            runsukuipercent = percent(
                                    errors[folder][el+'_mo_ukui'],
                                    diff
                                    )

            runsscipypercent = percent(
                                    errors[folder][el+'_mo_scipysem'],
                                    diff
                                    )

            # Plot percent uncertainties from multiple origins
            ax[1].plot(x, runsbatch5percent, 'b.')
            ax[1].plot(x, runsbatch10percent, 'r.')
            ax[1].plot(x, runsbatchlcorrpercent, 'g.')
            ax[1].plot(x, runsukuipercent, 'y+')
            ax[1].plot(x, runsscipypercent, 'kx')

            ax[1].set_ylabel('Diffusion MO Percent Error')
            ax[1].set_xlabel('Temperature [K]')
            ax[1].legend(handles=plotlabels, loc='upper right')
            ax[1].grid()

            # Save name for multiple origin uncertaintites
            name = (datadir +
                    '/' +
                    folder +
                    '/images/errormethods/errors/' +
                    'mo_' +
                    '_element_' +
                    el
                    )

            fig.tight_layout()
            fig.savefig(name)
            pl.close('all')

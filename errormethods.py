from matplotlib import pyplot as pl
from scipy import stats as st

from matplotlib import lines
from itertools import islice

from autocovariance import auto
from dfdiff import diffusionimport
from ukuiestimator import error as ukui
from batchmeans import error as batch

import pandas as pd
import numpy as np
import math
import os


def percent(x, y):
    return [i/j*100.0 for i, j in zip(x, y)]


datadir = '../export/'
exportdir = '../testpics/'

data = diffusionimport(datadir)
errors = {}
for folder in data:
    print(folder)

    errors[folder] = []
    for temp in data[folder]['origins']:
        cols = list(data[folder]['origins'][temp].columns.values)[1:]
        cols = [i for i in cols if 'err' not in i]

        regulardata = data[folder]['regular'][temp]
        modata = data[folder]['origins'][temp]

        errordf = {}
        for col in cols:
            k, r, index = auto(modata[col])

            approxtemp = str(math.ceil(temp))
            name = exportdir+folder+'_autocorrelation_temp_'+approxtemp+'_'+col
            pl.plot(k, r, 'b.', label=approxtemp+' [K]')
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

            errordf[col+'_diff'] = regulardata[col]
            errordf[col+'_fiterr'] = regulardata[col+'_err']
            errordf[col+'_mo_ukui'] = ukui(list(modata[col]))
            errordf[col+'_mo_batch(a=5)'] = batch(list(modata[col]), a=5)[0]
            errordf[col+'_mo_batch(a=10)'] = batch(list(modata[col]), a=10)[0]

            corbatch = batch(list(modata[col]), b=k[index])
            errordf[col+'_mo_batch(a=corbatch)'] = corbatch[0]

            errordf[col+'_mo_scipysem'] = st.sem(list(modata[col]))
            errordf[col+'_mo_fitavg'] = np.mean(list(modata[col+'_err']))

        errordf['temp'] = temp
        errordf = pd.DataFrame(errordf, index=[0])
        errors[folder].append(errordf)

for folder in data:
    errors[folder] = pd.concat(errors[folder])

batch5label = lines.Line2D(
                           [],
                           [],
                           color='b',
                           marker='.',
                           linestyle='None',
                           markersize=8,
                           label='Batch Means (a=5)'
                           )

batch10label = lines.Line2D(
                            [],
                            [],
                            color='r',
                            marker='.',
                            linestyle='None',
                            markersize=8,
                            label='Batch Means (a=10)'
                            )

batchlcorrlabel = lines.Line2D(
                               [],
                               [],
                               color='g',
                               marker='.',
                               linestyle='None',
                               markersize=8,
                               label='Batch Means (b=lcorr)'
                               )

ukuilabel = lines.Line2D(
                         [],
                         [],
                         color='y',
                         marker='+',
                         linestyle='None',
                         markersize=8,
                         label='Ukui Estimator'
                         )

scipylabel = lines.Line2D(
                          [],
                          [],
                          color='k',
                          marker='x',
                          linestyle='None',
                          markersize=8,
                          label='Scipy SEM'
                          )

plotlabels = []
plotlabels.append(batch5label)
plotlabels.append(batch10label)
plotlabels.append(batchlcorrlabel)
plotlabels.append(ukuilabel)
plotlabels.append(scipylabel)

size = (15, 5)

for folder in errors:

    cols = list(errors[folder].columns.values)
    elements = [i.split('_')[0] for i in cols if len(i.split('_')) > 1]
    elements = list(set(elements))

    for el in elements:
        fig, ax = pl.subplots(1, 2, figsize=size)

        x = errors[folder]['temp']

        ax[0].plot(x, errors[folder][el+'_diff'], 'b.')

        ax[0].set_ylabel('Diffusion [*10^-4 cm^2 s^-1]')
        ax[0].set_xlabel('Temperature [K]')
        ax[0].grid()

        ax[1].plot(x, errors[folder][el+'_fiterr'], 'r.')

        ax[1].set_ylabel('Diffusion Fit Error [*10^-4 cm^2 s^-1]')
        ax[1].set_xlabel('Temperature [K]')
        ax[1].grid()

        name = exportdir+folder+'_element_'+el
        fig.tight_layout()
        fig.savefig(name)
        pl.close(fig)

        fig, ax = pl.subplots(1, 2, figsize=size)

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
                                        errors[folder][el+'_mo_batch(a=corbatch)'],
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

        ax[1].plot(x, runsbatch5percent, 'b.')
        ax[1].plot(x, runsbatch10percent, 'r.')
        ax[1].plot(x, runsbatchlcorrpercent, 'g.')
        ax[1].plot(x, runsukuipercent, 'y+')
        ax[1].plot(x, runsscipypercent, 'kx')

        ax[1].set_ylabel('Diffusion MO Percent Error')
        ax[1].set_xlabel('Temperature [K]')
        ax[1].legend(handles=plotlabels, loc='upper right')
        ax[1].grid()

        name = exportdir+folder+'_mo_'+'_element_'+el
        fig.tight_layout()
        fig.savefig(name)
        pl.close(fig)

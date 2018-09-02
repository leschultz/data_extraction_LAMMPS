from PyQt5 import QtGui  # Added to be able to import ovito
from numpy.polynomial.polynomial import polyfit
from matplotlib import pyplot as pl
from single import analize as an
from scipy import stats as st

import pandas as pd
import numpy as np
import setup
import os

# Directories
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'
dump_directory = first_directory+'/../datacalculated/'

# Grab file names from the lammpstrj directory
names = os.listdir(data_directory+'lammpstrj/')

# Grab the run names
count = 0
for item in names:
    names[count] = item.split('.lammpstrj')[0]
    count += 1


def avg(*args, **kwargs):
    '''
    Do analysis for every run.
    '''

    series = args[0]

    print('_'*len(series))
    print('Analyzing all runs for the following:')
    print(series)
    print('-'*len(series))

    # Grab names that match the series input
    newnames = []
    for item in names:
        if series in item and series[0] == item[0]:
            newnames.append(item)

    # Gather plots, vibration, and MSD data for each run
    datamsd = {}
    datadif = {}
    fcc = []
    hcp = []
    bcc = []
    ico = []
    for name in newnames:
        run = an(name, *args[1:], **kwargs)

        data = run.calculate()  # Data calculated by ovito

        # Cluster Data
        fcc.append(data['fccavg'])
        hcp.append(data['hcpavg'])
        bcc.append(data['bccavg'])
        ico.append(data['icoavg'])

        run.plotrdf()  # Plot RDF
        run.plotmsd()  # Plot MSD
        run.plotclusters()  # Plot cluster time averages

        # Grab MSD data for all runs
        for key in data['msd']:
            if datamsd.get(key) is None:
                datamsd[key] = []
            datamsd[key].append(np.array(data['msd'][key]))

            # Calculate the diffusion values [*10^-4 cm^2 s^-1]
            if datadif.get(key) is None:
                datadif[key] = []

            slope = polyfit(data['time'], data['msd'][key], 1)[1]

            datadif[key].append(slope/6)

        # Try to generate graphs from txt file if available
        try:
            run.plotresponse()
        except Exception:
            pass

    # Step data from last iteration on previous loop
    time = data['time']

    print('Taking mean data')

    # Get the mean MSD for atom types and EIM
    meandatamsd = {}

    # Control the frequency of errorbars
    errorfreq = len(time)//10
    if errorfreq == 0:
        errorfreq = 1

    for key in datamsd:
        meandatamsd[key] = np.mean(datamsd[key], axis=0)
        meandatamsd[key+'_EIM'] = st.sem(datamsd[key])
        pl.errorbar(
                    time,
                    meandatamsd[key],
                    meandatamsd[key+'_EIM'],
                    errorevery=errorfreq,
                    label='Element Type: %s' % key
                    )

    pl.xlabel('Time [ps]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend(loc='upper left')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/averaged/motion/'+series+'_avgMSD')
    pl.clf()

    meandatadif = {}
    for key in datadif:
        meandatadif[key] = np.mean(datadif[key])
        meandatadif[key+'_EIM'] = st.sem(datadif[key])

    # Average the number of clusters accross runs
    clusters = {}
    clusters['fcc'] = np.mean(fcc)
    clusters['hcp'] = np.mean(hcp)
    clusters['bcc'] = np.mean(bcc)
    clusters['ico'] = np.mean(ico)

    print('\n')

    return time, meandatamsd, meandatadif, clusters

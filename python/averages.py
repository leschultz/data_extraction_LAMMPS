from PyQt5 import QtGui  # Added to be able to import ovito
from matplotlib import pyplot as pl
from single import analize as an

import pandas as pd
import numpy as np
import setup
import os

# Directories
first_directory = os.getcwd()
data_directory = first_directory+'/../data/'
dump_directory = data_directory+'analysis/'

# Grab file names from the lammpstrj directory
names = os.listdir(data_directory+'lammpstrj/')

# Grab the run names
count = 0
for item in names:
    names[count] = item.split('.lammpstrj')[0]
    count += 1


def eim(msd, mean_msd):
    ''' Take the error in the mean.'''

    # Save the number of columns and rows
    samples = len(msd)

    # Subtract each MSD at every time from the average and square it
    out = []
    for i in range(samples):
        value = np.subtract(msd[i], mean_msd)
        value **= 2
        out.append(value)

    # Get STD for each timepoint
    std_msd = (np.sum(out, axis=0)/samples)**0.5

    # Get error in the mean for each timepoint
    eim_msd = std_msd/(samples**0.5)

    # Return the error in the mean
    return eim_msd


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
    dataall = {}
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
            if dataall.get(key) is None:
                dataall[key] = []
            dataall[key].append(np.array(data['msd'][key]))

        # Try to generate graphs from txt file if available
        try:
            run.plotresponse()
        except Exception:
            pass

    # Step data from last iteration on previous loop
    time = data['time']

    print('Taking mean data')

    # Get the mean MSD for atom types and EIM
    data_mean = {}
    eim_data = {}

    # Control the frequency of errorbars
    errorfreq = len(time)//10
    if errorfreq == 0:
        errorfreq = 1

    for key in dataall:
        data_mean[key] = np.mean(dataall[key], axis=0)
        eim_data[key] = eim(dataall[key], data_mean[key])
        pl.errorbar(
                    time,
                    data_mean[key],
                    eim_data[key],
                    errorevery=errorfreq,
                    label='Element Type: %s' % key
                    )

    pl.xlabel('Time [ps]')
    pl.ylabel('MSD Averaged [A^2]')
    pl.legend(loc='upper left')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/motion/'+series+'_avgMSD')
    pl.clf()

    # The starting column for MSD data
    msdcolumns = [time]

    # The header for exported MSD data
    msdheader = 'time[ps] '
    msdfmt = '%f, '

    # Grab data for MSD and EIM
    for key in data_mean:
        msdcolumns.append(data_mean[key])
        msdheader += key+'MSD[A^2] '
        msdfmt += '%f, '
        msdcolumns.append(eim_data[key])
        msdheader += key+'EIM[A^2] '
        msdfmt += '%f, '

    # Save data in alternating oder of MSD and EIM (first is time)
    msdoutput = dump_directory+'msd/'+series+'_msd_average.txt'
    np.savetxt(
               msdoutput,
               np.transpose(msdcolumns),
               fmt=msdfmt,
               header=msdheader
               )

    # Average the number of clusters accross runs
    fccavg = np.mean(fcc)
    hcpavg = np.mean(hcp)
    bccavg = np.mean(bcc)
    icoavg = np.mean(ico)

    clusters = [fccavg, hcpavg, bccavg, icoavg]

    # The labels for clusters in the xlabel
    labels = ['FCC', 'HCP', 'BCC', 'ICO']
    location = [1, 2, 3, 4]

    count = 0
    for v, i in enumerate(clusters):
        pl.text(
                v+1, i,
                ' '+str(clusters[count]),
                color='red',
                ha='center',
                fontweight='bold'
                )

        count += 1

    pl.bar(location, clusters,  align='center')
    pl.xticks(location, labels)
    pl.xlabel('Cluster [-]')
    pl.ylabel('[count/(ps*size)]')
    pl.grid(b=True, which='both')
    pl.tight_layout()
    pl.savefig('../images/cluster/'+series+'_avgneighbor')
    pl.clf()

    clusterheader = 'FCC HCP BCC ICO'
    clusterfmt = '%f, %f, %f, %f'

    # Save the data for cluster in the neighbor folder
    clusteroutput = dump_directory+'cluster/'+series+'_cluster_average.txt'
    np.savetxt(
               clusteroutput,
               np.column_stack(clusters),
               header=clusterheader,
               fmt=clusterfmt
               )

    print('\n')

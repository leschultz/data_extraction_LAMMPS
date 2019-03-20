import pandas as pd
import numpy as np

df = pd.read_pickle('Tg.pkl')

# Average data by matching columns
columns = [
           'System',
           'Composition [decimal]',
           'Steps [-]',
           ]

dfgroup = df.groupby(columns)
dfenergygroup = dfgroup['Tg from E-3kT Curve [K]']
dfvolumegroup = dfgroup['Tg from Specific Volume Curve [K]']

# Column names for averages
avgenergycolumns = [
                    'System',
                    'Composition [decimal]',
                    'Steps [-]',
                    'Mean Tg from E-3kT Curve [K]',
                    'Std Tg from E-3kT Curve [K]',
                    'Number of Jobs with E-3kT Curve [K]',
                    'Number of Removed Jobs with E-3kT Curve [K]'
                    ]

dfenergyavg = pd.DataFrame(columns=avgenergycolumns)
count = 0
for etg in dfenergygroup:
    x = etg[1]
    n = len(x)
    mean = np.mean(x)
    std = np.std(x)
    xfiltered = x[abs(x-mean) < 2*std]
    nremoved = n-len(xfiltered)

    row = [etg[0][0], etg[0][1], etg[0][2]]

    row.append(np.mean(xfiltered))
    row.append(np.std(xfiltered))
    row.append(n)
    row.append(nremoved)

    dfenergyavg.loc[count] = row
    count += 1

# Column names for averages
avgvolumecolumns = [
                     'System',
                     'Composition [decimal]',
                     'Steps [-]',
                     'Mean Tg from Specific Volume Curve [K]',
                     'STD Tg from Specific Volume Curve [K]',
                     'Number of Jobs with Specific Volume Curve [K]',
                     'Number of Removed Jobs with Specific Volume Curve [K]'
                     ]

dfvolumeavg = pd.DataFrame(columns=avgvolumecolumns)
count = 0
for vtg in dfvolumegroup:
    x = vtg[1]
    n = len(x)
    mean = np.mean(x)
    std = np.std(x)
    xfiltered = x[abs(x-mean) < 2*std]
    nremoved = n-len(xfiltered)

    row = [vtg[0][0], vtg[0][1], vtg[0][2]]

    row.append(np.mean(xfiltered))
    row.append(np.std(xfiltered))
    row.append(n)
    row.append(nremoved)

    dfvolumeavg.loc[count] = row
    count += 1

dfavg = pd.merge(dfenergyavg, dfvolumeavg)

dfavg.to_html('Tgmeanfiltered.html')  # Export as an HTML table
dfavg.to_pickle('Tgmeanfiltered.pkl')  # Export as a pickle file

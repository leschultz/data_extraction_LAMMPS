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
                    'Number of Jobs with E-3kT Curve [K]'
                    ]

dfenergyavg = pd.DataFrame(columns=avgenergycolumns)
count = 0
for etg in dfenergygroup:
    row = [etg[0][0], etg[0][1], etg[0][2]]
    row.append(etg[1].mean())
    row.append(etg[1].std(ddof=0))
    row.append(etg[1].shape[0])

    dfenergyavg.loc[count] = row
    count += 1

# Column names for averages
avgvolumecolumns = [
                     'System',
                     'Composition [decimal]',
                     'Steps [-]',
                     'Mean Tg from Specific Volume Curve [K]',
                     'STD Tg from Specific Volume Curve [K]',
                     'Number of Jobs with Specific Volume Curve [K]'
                     ]

dfvolumeavg = pd.DataFrame(columns=avgvolumecolumns)
count = 0
for vtg in dfvolumegroup:
    row = [vtg[0][0], vtg[0][1], vtg[0][2]]
    row.append(vtg[1].mean())
    row.append(vtg[1].std(ddof=0))
    row.append(vtg[1].shape[0])

    dfvolumeavg.loc[count] = row
    count += 1

dfavg = pd.merge(dfenergyavg, dfvolumeavg)

dfavg.to_html('Tgmean.html')  # Export as an HTML table
dfavg.to_pickle('Tgmean.pkl')  # Export as a pickle file

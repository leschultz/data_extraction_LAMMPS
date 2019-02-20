from infoparser import inputinfo

from matplotlib import pyplot as pl
from io import BytesIO

import pandas as pd
import numpy as np

import tarfile
import math
import os

# The path to the google drive data
path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/La-Al/Al1.00/667/job1'
#path = '/home/nerve/Documents/UW/gdrive/DMREF/MD/Rc_database/TEMP/Al-Ag/Ag1.00/667/job1'

# Look for all directories as generator object
paths = os.walk(path)

# Define the percent of data for the fits
top = 50.0
bottom = 15.0

# Loop for each path
for item in paths:

    try:

        if 'job' in item[0]:

            # Were parsed data will be stored
            data = []

            # Create a name from the path
            name = item[0].split('/')
            name = name[-4:]
            name = os.path.join(*name)
            print(name)

            # Grab the output archive file that contains run system data
            filename = os.path.join(*[item[0], 'outputs.tar.gz'])
            inputfile = os.path.join(*[item[0], 'dep.in'])

            # Some of the parameters from the LAMMPS input file
            param = inputinfo(inputfile)
            hold1 = param['hold1']

            # Open the archive
            archive = tarfile.open(filename, 'r')

            # Iterate for each file in the archive
            for member in archive.getmembers():

                # Open the file containing system data
                if '.out' in  str(member):
                    content = (archive.extractfile(member)).read()
                    content = content.splitlines()

                    # Parse information in file
                    count = 0  # Counter for headers later
                    for line in content:

                        # Bunch of parsing
                        line = line.decode('utf-8')
                        line = line.split(' ')
                        line = [i for i in line if '' != i]

                        if line:
                            if (line[0] == 'Step' and count == 0):
                                headers = line
                                count = 1

                            if ('Created' in line and 'atoms' in line):
                                natoms = int(line[1])

                            try:
                                    line = [float(i) for i in line]
                                    data.append(line)

                            except Exception:
                                pass

            # System data as a dataframe with removed repeated steps
            dfsystem = pd.DataFrame(data, columns=headers)
            dfsystem = dfsystem.drop_duplicates('Step')
            dfsystem = dfsystem.reset_index(drop=True)

            # Parsed data exported from LAMMPS
            dfsystem = dfsystem.loc[dfsystem['Step'] >= hold1]  # Start of run
            dfenergy = dfsystem[['Temp', 'Volume']]  # Energies and Temperatures
            dfenergy.loc[:, 'Volume'] = dfenergy['Volume'].divide(natoms)

            xdata = list(dfenergy['Temp'])
            ydata = list(dfenergy['Volume'])

            # Fit the higher temperature range
            length = len(xdata)
            start0 = 0
            end0 = math.floor((top/100)*length)

            x0 = xdata[start0:end0]
            y0 = ydata[start0:end0]
            fit0 = np.polyfit(x0, y0, 1)
            fitf0 = np.poly1d(fit0)
            yfit0 = fitf0(xdata)

            fitrange0 = str([math.floor(xdata[start0]), math.floor(xdata[end0])])

            # Fit the lower temperature range
            start1 = math.ceil((1-bottom/100)*length)
            end1 = -1
            x1 = xdata[start1:end1]
            y1 = ydata[start1:end1]

            fit1 = np.polyfit(x1, y1, 1)
            fitf1 = np.poly1d(fit1)
            yfit1 = fitf1(xdata)

            fitrange1 = str([math.floor(xdata[start1]), math.floor(xdata[end1])])

            fig, ax = pl.subplots()

            ax.plot(xdata, ydata, '.')
            ax.plot(xdata, yfit0, 'r', label='Fit Range of '+fitrange0+' [K]')
            ax.plot(xdata, yfit1, 'g', label='Fit Range of '+fitrange1+' [K]')

            if not os.path.exists(name):
                os.makedirs(name)
            savepath = os.path.join(*['./', name])

            try:
                npoints = 2
                point = [0]*(npoints+1)  # A point larger than 1 to start with
                tolerance = abs(max(ydata)-min(ydata))  # The initial tolerance

                # Iterate until point of intersection is found between fits
                count = 0
                while len(point) > npoints:
                    condition = np.isclose(yfit0, yfit1, atol=tolerance)
                    point = np.argwhere(condition).reshape(-1)
                    tolerance -= tolerance/10

                    if count > 100:
                        break

                    count += 1

                temps = np.array(xdata)[point]
                temp = sum(temps)/len(temps)  # Average if len > 1
                ax.axvline(
                           x=temp,
                           linestyle='--',
                           label='Fit Intersection at '+str(temp)[:5]+' [K]'
                           )

                # Export Tg
                with open(savepath+'/tg.txt', 'w') as file:
                    file.write('{}'.format(str(temp)+' K'))

            except Exception:
                pass

            dfenergy.to_csv(
                            savepath+'/tg_energy.txt',
                            sep=' ',
                            index=False
                            )

            imagepath = savepath+'/tg_energy.png'

            ax.set_xlabel('Temperature [K]')
            ax.set_ylabel('Specific Volume [A^3/atom]')
            ax.grid()
            ax.legend(loc='best')
            plot = ax.get_figure()
            plot.tight_layout()
            plot.savefig(imagepath)
            pl.close('all')

    except Exception:
        print(item, 'problem')
        pass

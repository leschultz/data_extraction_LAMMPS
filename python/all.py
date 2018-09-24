from PyQt5 import QtGui  # Added to be able to import ovito
from nameparser import parse
from single import analize

import os

# Directories
firstdir = os.getcwd()
lammpstrjdir = firstdir+'/../data/lammpstrj/'

# Grab the file names from the lammpstrj directory
names = os.listdir(lammpstrjdir)

# Grab the names of runs to be averaged
count = 0
for name in names:
    names[count] = name.split('.lammpstrj')[0]
    count += 1

for item in names:

    points, timestep, dumprate = parse(item)

    # Do averaging for files
    value = analize(
                    item,
                    points[1],
                    points[2],
                    timestep,
                    dumprate,
                    [points[0], points[1], points[2]],
                    10,
                    50
                    )

    data = value.calculate()
    value.plotmsd()
    value.plotrdf()
    value.msdsave()
    value.rdfsave()
    value.diffusionsave()

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

    value.calculate_time()
    value.calculate_msd()
    value.calculate_rdf()
    value.calculate_diffusion()
    value.multiple_origins_diffusion()
    data = value.calculation_export()
    value.plot_msd()
    value.plot_rdf()
    value.save_msd()
    value.save_rdf()
    value.save_multiple_origins_diffusion()
    value.save_diffusion()

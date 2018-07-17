import matplotlib.pyplot as pl
from scipy import mean
from glob import glob
import re
import os

directory = os.getcwd()
directories = glob(directory+'/*/')

# Data that will hold distances
data = {}

# Loop for viewing files
def file_looper(file_number):
    for item in directories:
        os.chdir(directory+'/data/lammpstrj')
        path, dirs, files = next(
                                 os.walk(directory+
                                 '/data/lammpstrj')
                                 )
        return files

# Create key names from first directory
file_names = file_looper(1)

for name in file_names:
    if re.match('distance_*',name):
        data[name]=[]

# Append data to keys
count = 1
for item in directories:
    os.chdir(directory+'/motion_curves'+str(count)+'/python')
    for name in file_looper(count):
        if re.match('distance_*',name):
            fileread = open(str(name),'r')
            data[name].append(float(fileread.read()))
    count += 1

data_averages = {}
for key, value in data.iteritems():
    data_averages[key] = mean(value)

temperatures = [900, 910, 920, 930, 933, 940, 950, 960, 970, 980, 990, 1000]

average_mobility = [
                    data_averages['distance_traveled_average900'],
                    data_averages['distance_traveled_average910'],
                    data_averages['distance_traveled_average920'],
                    data_averages['distance_traveled_average930'],
                    data_averages['distance_traveled_average933'],
                    data_averages['distance_traveled_average940'],
                    data_averages['distance_traveled_average950'],
                    data_averages['distance_traveled_average960'],
                    data_averages['distance_traveled_average970'],
                    data_averages['distance_traveled_average980'],
                    data_averages['distance_traveled_average990'],
                    data_averages['distance_traveled_average1000']
                    ]

pl.plot(temperatures, average_mobility)
pl.xlabel('Temperatures [K]')
pl.ylabel('Distance Traveled [A]')
pl.show()

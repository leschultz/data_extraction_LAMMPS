import matplotlib.pyplot as pl
from scipy import mean
from glob import glob
import re
import os

first_directory = os.getcwd()
data_directory = first_directory+'/../data/analysis/'
os.chdir(data_directory)

# Data that will hold distances
data = {}

# The names of mean dislacements for each run
file_names = os.listdir(data_directory)

# The temperatures from each run extrated from file name
temperatures = {}
separator = 'K'
for item in file_names:
    value = item[26:item.find(separator)]
    temperatures.update({value: []})

# Appending distances for each temperature run
for item in file_names:
    value = item[26:item.find(separator)]
    fileread = open(str(item), 'r')
    temperatures[value].append(float(fileread.read()))

# Taking the averages of distances
data_means = {}
for key, value in temperatures.iteritems():
    data_means[key] = mean(value)

temp = []
dist = []
for key, value in data_means.iteritems():
    temp.append(float(key))
    dist.append(data_means[key])

pl.plot(temp, dist, 'b*')
pl.xlabel('Temperature [K]')
pl.ylabel('Distance Traveled [A]')
pl.show()

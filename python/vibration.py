from matplotlib import pyplot as pl

import pandas as pd
import numpy as np
import os

# Get directories
first_directory = os.getcwd()
data_directory = first_directory+'/../data/lammpstrj/'

# Change into the lammpstrj directory
os.chdir(data_directory)

# Load data
data = pd.read_csv('300K_1_rate.lammpstrj')
print(data)

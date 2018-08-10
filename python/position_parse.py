import pandas as pd
import numpy as np
import os

def trj(name):
	'''
	This function extracts the trajectories for each simulation atom.
	'''

	# Get directories
	first_directory = os.getcwd()
	data_directory = first_directory+'/../data/lammpstrj/'
	dump_directory = first_directory+'/../data/analysis/'

	# Change into the lammpstrj directory
	os.chdir(data_directory)

	# Load data
	mycolumns = [0, 1, 2, 3, 4, 5, 6]
	data = pd.read_csv(name, names=mycolumns, sep=' ')

	# Number of atoms
	number = int(data[0][3])

	# Data lenght not containing positions
	drop_length = 9

	# Change in step which assumes the first step is zero	
	frequency = int(data[0][number+drop_length+1])

	# The number of rows for unchanged data
	rows = data.shape[0]

	# Define rows to drop that do not have trajectories
	drop = []
	step = []
	count = 0
	for i in range(0, rows, number+drop_length):
		drop += list(range(i, i+drop_length))
		step += list(np.zeros((number), dtype=int)+count)
		count += frequency

	# Drops the rows defined from data
	data = data.drop(data.index[drop])
	data = data.drop(data.columns[-2:], axis=1)
	data = data.reset_index(drop=True)
	data.columns = ['atom', 'element', 'xu', 'yu', 'zu']
	data.insert(loc=0, column='step', value=step)

	# change values to integers or floats
	data.atom = data.atom.apply(int)
	data.element = data.element.apply(int)
	data.xu = data.xu.apply(float)
	data.yu = data.yu.apply(float)
	data.zu = data.zu.apply(float)

	return frequency, data

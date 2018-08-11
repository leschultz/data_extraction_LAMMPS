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

	# Change into the lammpstrj directory
	os.chdir(data_directory)

	# Load data
	mycolumns = [0, 1, 2, 3, 4, 5, 6]
	data = pd.read_csv(name, names=mycolumns, sep=' ')

	# Number of atoms
	atoms = int(data[0][3])

	# Data lenght not containing positions
	drop_length = 9

	# Change in step which assumes the first step is zero
	frequency = int(data[0][atoms+drop_length+1])

	# The number of rows for unchanged data
	rows = data.shape[0]

	# Define rows to drop that do not have trajectories
	drop = []
	step = []
	count = 0
	for i in range(0, rows, atoms+drop_length):
		drop += list(range(i, i+drop_length))
		step += list(np.zeros((atoms), dtype=int)+count)
		count += frequency

	# Format data
	data = data.drop(data.index[drop])  # Drop specified rows
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

	# The final step of the run
	finalstep = max(step)

	# Change back to original directory
	os.chdir(first_directory)

	return atoms, frequency, finalstep, data


def rdf(name):
	'''
	Extract the radial distribution (RDF) data.
	'''

	# Grab relevant directories
	first_directory = os.getcwd()
	data_directory = first_directory+'/../data/rdf/'

	# Change into the lammpstrj directory
	os.chdir(data_directory)

	# Load data
	mycolumns = [0, 1, 2, 3]
	data = pd.read_csv(name, names=mycolumns, skiprows=3, sep=' ')

	rows = data.shape[0]

	# Number of bins
	bins = int(data[1][0])

	# Data acquisition frequency (steps/acqusition)
	frequency = int(data[0][1+bins])

	# Define rows to drop that do not have trajectories
	drop = []
	step = []
	count = 0
	for i in range(0, rows, bins+1):
		drop.append(i)
		step += list(np.zeros((bins), dtype=int)+count)
		count += frequency

	# Format data
	data = data.drop(data.index[drop])  # Drop specified rows
	data.columns = ['bins', 'center', 'rdf', 'coord_r']
	data.insert(loc=0, column='step', value=step)

    # change values to integers or floats
	data.step = data.step.apply(int)
	data.bins = data.bins.apply(int)
	data.center = data.center.apply(float)
	data.rdf = data.rdf.apply(float)
	data.coord_r = data.coord_r.apply(float)

	# Return to the first directory
	os.chdir(first_directory)

	return bins, data

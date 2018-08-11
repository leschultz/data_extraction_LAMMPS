from matplotlib import pyplot as pl
from position_parse import trj
import numpy as np

#pl.switch_backend('agg')

def difference(i, j):
	'''Subtracts the past value j from the future value i'''

	return [i-j for (i, j) in zip(i, j)]


def displacement(dx, dy, dz):
	'''Takes the displacement in three dimensions.'''

	return [(dx**2+dy**2+dz**2)**0.5 for (dx, dy, dz) in zip(dx, dy, dz)]


class analize(object):
	'''Computation functions are defined here'''

	def __init__(self, name):
		'''Load data'''

		self.run = str(name).split('.')[0]  # The name of the run
		self.tem = trj(name)  # Load
		self.num = self.tem[0]  # Number of atoms
		self.frq = self.tem[1]  # Acquistion Frequency (steps/acqusition)
		self.trj = self.tem[2]  # Trajectories

	def vibration(self, start, stop, plot=True):
		'''
		This function calculates vibration displacements.
		The start and end are inclusive.
		'''

		run = self.run  # The run used
		numb = self.num  # Number of atoms
		data = self.trj  # Trajectory data
		freq = self.frq  # Acqusition rate

		# The last recorded step
		last_step = max(data.step)

		# Raise errors before loaing data for efficienyc in the future
		# Check to see if beyond data limmit
		if start > last_step:
			raise NameError('Start is beyond data length')

		# Check to see if the input is valid
		if start % freq == 1:
			raise NameError('Start is not a multiple of the data acquisition rate')

		# Check if end goes beyond data range
		if stop > last_step:
			raise NameError('Cannot gather more data than specified')

		# Check if end is valid point
		if stop % freq == 1:
			raise NameError('End is not a multiple of the data acqusition rate')

		# Find the displacements due to vibration between each timestep
		step_recorded = []
		x = []
		y = []
		z = []
		for i in range(start, stop+1, freq):
			index = data.index[data.step == i].tolist()
			
			x.append(data.xu[index].values.tolist())  # x positions
			y.append(data.yu[index].values.tolist())  # y positions
			z.append(data.zu[index].values.tolist())  # z positions

			step_recorded.append(i)  # Time step

		# Averages between start and stop
		x_mean = np.mean(x, axis=0)  # Average x values
		y_mean = np.mean(y, axis=0)  # Average y values
		z_mean = np.mean(z, axis=0)  # Average z values

		# Take displacement of the averages with respect to (0,0,0)
		mean_positions = displacement(x_mean, y_mean, z_mean)

		# Take the distance from the mean position
		vibrations = []
		for i in range(0, len(x)):
			for j in range(0, numb+1):
				pos = displacement(x[i], y[i], z[i])
				pos_diff = difference(pos, mean_positions)
				pos_sqrd = [k**2 for k in pos_diff]
				pos_mean = np.mean(pos_sqrd)

			vibrations.append(pos_mean)
		
		if plot == True:
			pl.plot(step_recorded, vibrations)
			pl.xlim([start, stop])
			pl.xlabel('Step [-]')
			pl.ylabel('Mean Squared Vibration [A^2]')
			pl.legend([run])
			pl.grid(True)
			pl.tight_layout()
			pl.show()

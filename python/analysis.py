from matplotlib import pyplot as pl
from position_parse import trj
import numpy as np

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
		self.frq = self.tem[0]  # Acquistion Frequency (steps/acqusition)
		self.trj = self.tem[1]  # Trajectories

	def vibration(self, start, plot=True):
		'''
		This function calculates vibration displacements.
		'''

		run = self.run  # The run used
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

		# Find the displacements due to vibration between each timestep
		disp_mean = []
		step_recorded = []
		for i in range(start, last_step, freq):
			index0 = data.index[data.step == i].tolist()
			index1 = data.index[data.step == i+freq].tolist()
			
			x0 = data.xu[index0].values  # Past x positions
			x1 = data.xu[index1].values  # Future x positions
			dx = difference(x1, x0)  # Difference in x coordinates
			
			y0 = data.yu[index0].values  # Past y positions
			y1 = data.yu[index1].values  # Future y positions
			dy = difference(y1, y0)  # Difference in y coordinates

			z0 = data.zu[index0].values  # Past z positions
			z1 = data.zu[index1].values  # Future z positions
			dz = difference(z1, z0)  # Difference in z coordinates

			disp = displacement(dx, dy, dz)  # Displacement for each atom

			disp_mean.append(np.mean(disp))  # Mean displacement for all steps
			step_recorded.append(i)  # Time step

		if plot == True:
			pl.plot(step_recorded, disp_mean)
			pl.xlabel('Step [-]')
			pl.ylabel('Vibration [A]')
			pl.legend([run])
			pl.grid(True)
			pl.tight_layout()
			pl.show()

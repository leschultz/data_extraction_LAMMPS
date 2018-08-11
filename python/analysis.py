from matplotlib import pyplot as pl

import dataparse as da
import numpy as np

pl.switch_backend('agg')


def difference(i, j):
	'''Subtracts the past value j from the future value i'''

	return [i-j for (i, j) in zip(i, j)]


def displacement(dx, dy, dz):
	'''Takes the displacement in three dimensions.'''

	return [(dx**2+dy**2+dz**2)**0.5 for (dx, dy, dz) in zip(dx, dy, dz)]


class analize(object):
	'''Computation functions are defined here'''

	def __init__(self, name, start, stop):
		'''Load data'''

		self.run = name  # The name of the run
		self.trjout = da.trj(self.run+'.lammpstrj')  # Load trajectories
		self.num = self.trjout[0]  # Number of atoms
		self.frq = self.trjout[1]  # Acquistion Frequency (steps/acqusition)
		self.lst = self.trjout[2]  # Last recorded step
		self.trj = self.trjout[3]  # Trajectories

		self.rdfout = da.rdf(self.run+'.rdf')  # Load RDF data
		self.bins = self.rdfout[0]
		self.rdfdata = self.rdfout[1]

		# Inclusive start and stop conditions
		self.start = start  # Start Step
		self.stop = stop  # Stop step

		# Check to see if beyond data limmit
		if self.start > self.lst:
			raise NameError('Start is beyond data length')

		# Check to see if the input is valid
		if self.start % self.frq == 1:
			raise NameError('Start is not a multiple of the data acquisition rate')

		# Check if end goes beyond data range
		if self.stop > self.lst:
			raise NameError('Cannot gather more data than specified')

		# Check if end is valid point
		if self.stop % self.frq == 1:
			raise NameError('End is not a multiple of the data acqusition rate')

	def vibration(self, plot=True):
		'''
		This function calculates vibration displacements.
		The start and end are inclusive.
		'''

		# The last recorded step
		last_step = max(self.trj.step)

		# Find the displacements due to vibration between each timestep
		self.steprecorded = []
		x = []
		y = []
		z = []
		for i in range(self.start, self.stop+1, self.frq):
			index = self.trj.index[self.trj.step == i].tolist()

			x.append(self.trj.xu[index].values.tolist())  # x positions
			y.append(self.trj.yu[index].values.tolist())  # y positions
			z.append(self.trj.zu[index].values.tolist())  # z positions

			self.steprecorded.append(i)  # Time step

		# Averages between start and stop
		x_mean = np.mean(x, axis=0)  # Average x values
		y_mean = np.mean(y, axis=0)  # Average y values
		z_mean = np.mean(z, axis=0)  # Average z values

		# Take displacement of the averages with respect to (0,0,0)
		mean_positions = displacement(x_mean, y_mean, z_mean)

		# Take the distance from the mean position
		vibrations = []
		for i in range(0, len(x)):
			for j in range(0, self.num+1):
				pos = displacement(x[i], y[i], z[i])
				pos_diff = difference(pos, mean_positions)
				pos_sqrd = [k**2 for k in pos_diff]
				pos_mean = np.mean(pos_sqrd)

			vibrations.append(pos_mean)

		if plot is True:
			pl.plot(self.steprecorded, vibrations)
			pl.xlabel('Step [-]')
			pl.ylabel('Mean Squared Vibration [A^2]')
			pl.legend([self.run])
			pl.grid(True)
			pl.tight_layout()
			pl.savefig('../images/motion/'+self.run+'_vibration')
			pl.clf()

	def msd(self, plot=True):
		'''
		Calcualte the means squared displacement.
		'''

		# The initial position of each atom
		index0 = self.trj.index[self.trj.step == self.start].tolist()
		x0 = self.trj.xu[index0].values.tolist()
		y0 = self.trj.yu[index0].values.tolist()
		z0 = self.trj.zu[index0].values.tolist()

		# Gather the distance from the start at each timestep
		msd = []
		for i in range(self.start, self.stop+1, self.frq):
			index = self.trj.index[self.trj.step == i].tolist()

			x = self.trj.xu[index].values.tolist()  # x trajectories
			y = self.trj.yu[index].values.tolist()  # y trajectories
			z = self.trj.zu[index].values.tolist()  # z trajectories

			dx = difference(x, x0)  # Change from initial x
			dy = difference(y, y0)  # Change from initial y
			dz = difference(z, z0)  # Change from initial z

			pos = displacement(dx, dy, dz)  # Absolute positions
			pos_sqrd = [j**2 for j in pos]  # Squared positions
			msd.append(np.mean(pos_sqrd))  # Mean of squared positions

		if plot is True:
			pl.plot(self.steprecorded, msd)
			pl.xlabel('Step [-]')
			pl.ylabel('Mean Squared Displacement [A^2]')
			pl.legend([self.run])
			pl.grid(True)
			pl.tight_layout()
			pl.savefig('../images/motion/'+self.run+'_msd')
			pl.clf()

	def rdf(self, step=None, plot=True):
		'''
		Plot the radial distribution at a point and throughout time.
		'''

		# Gather all the steps where data was recorded
		allsteps = list(set(self.rdfdata.step.values.tolist()))
		allsteps = sorted(allsteps, key=int)

		# The center of bins
		bincenters = list(set(self.rdfdata.center.values.tolist()))
		bincenters = sorted(bincenters, key=float)

		for i in list(range(1, self.bins+1)):
			index = self.rdfdata.index[self.rdfdata.bins == i].tolist()
			binsdata = self.rdfdata.rdf[index].values.tolist()
			pl.plot(
                    allsteps,
                    binsdata,
                    label="Center [A] %1.2f" % (bincenters[i-1],))

		pl.xlabel('Step [-]')
		pl.ylabel('g(r)')
		pl.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0)
		pl.grid(True)
		pl.tight_layout()
		pl.savefig('../images/rdf/'+self.run+'_allrdf')
		pl.clf()

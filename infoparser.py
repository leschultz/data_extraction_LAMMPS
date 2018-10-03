import os


class parameters(object):
    '''
    Class to grab relevant files and data for computation.
    '''

    def __init__(self, path):

        self.path = path  # The data folder path
        self.inputfiles = {}  # All data is stored here
        self.parameters = {}  # Relevant paramters for each trajectory file

    def files(self):
        '''
        Grab the trajectory and input file names with the path.
        '''

        folders = os.listdir(self.path)

        inputs = []
        trajectories = []
        for folder in folders:
            directory = self.path+'/'+folder+'/'

            inputs.append(directory+'dep.in')
            trajectories.append(directory+'uwtraj.lammpstrj')

        self.input_files = inputs
        self.trajectory_files = trajectories

    def inputinfo(self):
        '''
        Parse the input file to grab run information.
        '''

        count = 0
        for item in self.input_files:

            runsteps = []
            with open(item) as file:
                for line in file:
                    value = line.strip().split(' ')

                    if 'timestep' in value[0]:
                        for i in value:
                            try:
                                timestep = float(i)
                            except Exception:
                                pass

                    if 'dump' in value:
                        for i in value:
                            try:
                                dumprate = int(i)
                            except Exception:
                                pass

                    if 'run' in value:
                        for i in value:
                            try:
                                runsteps.append(int(i))
                            except Exception:
                                pass

                    if 'imax' in value:
                        for i in value:
                            try:
                                iterations = int(i)
                            except Exception:
                                pass

                    if 'tfi' in value:
                        tfi = value[-1]
                        tfi = tfi.split('-${i}*')
                        tempstart = float(tfi[0])
                        deltatemp = float(tfi[1])

            increment = sum(runsteps[-2:])

            hold1 = sum(runsteps[:-2])
            hold2 = runsteps[-2]
            hold3 = runsteps[-1]

            traj = self.trajectory_files[count]
            count += 1

            self.parameters[traj] = {
                                     'timestep': timestep,
                                     'dumprate': dumprate,
                                     'hold1': hold1,
                                     'hold2': hold2,
                                     'hold3': hold3,
                                     'iterations': iterations,
                                     'tempstart': tempstart,
                                     'deltatemp': deltatemp,
                                     'increment': increment
                                     }

        return self.parameters

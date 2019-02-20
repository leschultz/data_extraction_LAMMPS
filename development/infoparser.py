'''
Find pertinent information in LAMMPS input files.
'''

def inputinfo(item):
    '''
    Parse the input file to grab run information.
    '''

    # Open file and iterate per line
    runsteps = []
    with open(item) as file:
        for line in file:
            value = line.strip().split(' ')

            # Find timestep if word in line
            if 'timestep' in value[0]:
                for i in value:
                    try:
                        timestep = float(i)
                    except Exception:
                        pass

            # Find the dump rate if word in line
            if 'dump' in value:
                for i in value:
                    try:
                        dumprate = int(i)
                    except Exception:
                        pass

            # Find all defined run steps and save under runsteps
            if 'run' in value:
                for i in value:
                    try:
                        runsteps.append(int(i))
                    except Exception:
                        pass

            # The number of steps for contant temperatures
            if 'imax' in value:
                for i in value:
                    try:
                        iterations = int(i)
                    except Exception:
                        pass

            # Determine the drop in temperature between steps
            if 'tfi' in value:
                tfi = value[-1]
                tfi = tfi.split('-${i}*')
                tempstart = float(tfi[0])
                deltatemp = float(tfi[1])
                tempstart -= deltatemp

        increment = sum(runsteps[-2:])  # The steps to the start of hold

        hold1 = sum(runsteps[:-2])  # The steps until temperature steps
        hold2 = runsteps[-2]  # The start of hold
        hold3 = runsteps[-1]  # The end of hold

        # Save paramters for each trajectory file
        parameters = {
                      'timestep': timestep,
                      'dumprate': dumprate,
                      'hold1': hold1,
                      'hold2': hold2,
                      'hold3': hold3,
                      'iterations': iterations,
                      'tempstart': tempstart,
                      'deltatemp': deltatemp,
                      'increment': increment,
                      }

    return parameters

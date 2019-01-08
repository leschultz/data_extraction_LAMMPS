'''
Apply the diffusion and RDF analysis for all steps in a run.
'''

from PyQt5 import QtGui  # Added to be able to import ovito
from physical.singlestep import analize


def run(param, exportdir):
    '''
    Iterate initial data analysis for all steps in all runs
    '''

    # Apply for each run in the main directory
    for item in param:
        filename = item

        printname = 'Gathering Data from File: '+filename

        # Print on screen the run analyzed
        print('-'*len(printname))
        print(printname)
        print('-'*len(printname))

        # Parsed parameters
        n = param[item]['iterations']
        increment = param[item]['increment']
        deltatemp = param[item]['deltatemp']
        starttemp = param[item]['tempstart']
        timestep = param[item]['timestep']
        dumprate = param[item]['dumprate']
        hold2 = param[item]['hold2']
        hold3 = param[item]['hold3']

        # The path to save in
        savepath = exportdir+'/'+item.split('/')[-2]

        # Apply settle analysis on each step of run
        for iteration in list(range(0, n)):

            print(
                  'Temperature step: ' +
                  str(starttemp-iteration*deltatemp) +
                  ' [K]'
                  )

            # Find the start of quench to the next step
            hold1 = param[item]['hold1']
            hold1 += iteration*increment

            # Start of quench, start of hold, and end of hold
            points = [hold1, hold1+hold2, hold1+hold2+hold3]

            # Start the method for data analysis for the step
            value = analize(
                            item,
                            savepath,
                            points[1],
                            points[2],
                            timestep,
                            dumprate,
                            [points[0], points[1], points[2]],
                            10,
                            50
                            )

            value.calculate_time()  # Time normalized
            value.calculate_msd()  # Mean Squared Displacement
            value.calculate_rdf()  # Radial Distribution Function
            value.calculate_diffusion()  # Diffusion from linear fit
            value.multiple_origins_diffusion()  # Diffusion Multiple Origins
            data = value.calculation_export()  # Grab data calculated

            # Save name convention
            savename = (
                        item.split('/')[-2] +
                        '_' +
                        str(starttemp-iteration*deltatemp).split('.')[0] +
                        'K'
                        )

            # Plot relevant plots
            value.plot_msd(savename)
            value.plot_diffusion(savename)
            value.plot_rdf(savename)

            # Save relevant data
            value.save_msd(savename)
            value.save_rdf(savename)
            value.save_multiple_origins_diffusion(savename)
            value.save_diffusion(savename)

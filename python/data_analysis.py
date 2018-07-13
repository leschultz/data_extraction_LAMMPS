import matplotlib.pyplot as pl
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Terminal execution of the tool.',
                                 usage='Create plots.',
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 )
help_temperature_anneal = (
        """Plot the values for the annealing temperature
        """
        )

parser.add_argument('-n',
                    type=int,
                    nargs='+',
                    help=help_temperature_anneal,
                    )

args = parser.parse_args()

for item in args.n:
    data = pd.read_csv(
                       '../data/'+str(item)+'.txt',
                       comment='#',
                       sep=' ',
                       skiprows=1,
                       header=None
                       )

    data.columns = ([
                     'time step',
                     'temperature',
                     'pressure',
                     'volume',
                     'potential energy',
                     'kinetic energy'
                     ])

    pl.plot(data['time step'], data['temperature'])
    pl.xlabel('Time Step [fs]')
    pl.ylabel('Temperature [K]')
    pl.legend([str(item)+' [K] annealing'])
    pl.grid(True)
    pl.savefig('../images/'+str(item))
    pl.clf()

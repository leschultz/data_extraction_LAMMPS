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
                     help=help_temperature_anneal,
                    )

args = parser.parse_args()

data = pd.read_csv(
        '../data/'+str(args.n)+'.txt',
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
pl.grid(True)
pl.savefig('../images/'+str(args.n))

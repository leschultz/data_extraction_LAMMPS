import matplotlib.pyplot as pl
import pandas as pd

data = pd.read_csv(
                   'data.txt',
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
pl.show()

import matplotlib.pyplot as pl
import pandas as pd

data = pd.read_csv(
                   '../data/data_characteristics.txt',
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
pl.show()

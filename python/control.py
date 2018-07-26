import propensity_for_motion
import plots_over_time
import plots_analysis
import analysis
import setup

# Check for needed directories at start
setup.setup()


class control(object):
    '''A class for controlling the sequence of scripts run'''

    def __init__(self, initial_skip, stop):
        self.initial_skip = initial_skip
        self.stop = stop

    def analyze(initial_skip, stop):
        print('Crunching data')
        analysis.analyze(initial_skip)
        propensity_for_motion.propensity(stop)

    def plot_system():
        print('Plotting data from systems')
        plots_over_time.plot()

    def plot_analysis(stop):
        print('Plotting the analysis data')
        plots_analysis.plot(stop)

    def clean():
        print('Deleting all data')
        setup.clean()

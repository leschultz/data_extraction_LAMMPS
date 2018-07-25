import plots_over_time
import plots_analysis
import analysis
import setup

# Check for needed directories at start
setup.setup()


class control(object):
    '''A class for controlling the sequence of scripts run'''

    def analyze():
        print('Crunching data')
        analysis.analyze()

    def plots_system():
        print('Plotting data from systems')
        plots_over_time.plot()

    def plots_analysis():
        print('Plotting the analysis data')
        plots_analysis.plot()

    def clean():
        print('Deleting all data')
        setup.clean()

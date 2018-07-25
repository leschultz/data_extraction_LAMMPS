import plots_over_time
import plots_analysis
import analysis


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

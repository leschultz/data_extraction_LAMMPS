A detailed description for each function is written within each function.

Before using the tool, python setup.py needs to be run.

analysis.py can be used as below

	Usage: python3 -c 'from analysis import analize as an; run = an(<file>, <start step, <end step>); run.vibration(); value = run.msd(); run.rdf(<step>); run.response()'

	Example: python3 -c 'from analysis import analize as an; run = an("900K_1", 130000, 169000); run.vibration(); value = run.msd(); run.rdf(130000); run.response()'

averages.py can be used to attain the averages between MSDs and it executes analysis.py for all runs specifed in series. The variable value stores teh return value for steps and mean MSD.

	Usage: python3 -c 'from averages import avg; value = avg(<Temperature>, <start step>, <end step>, <step>)'

	Example: python3 -c 'from averages import avg; value = avg("300K", 10000+34000, 10000+34000+10000, 10000)'

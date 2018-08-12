A detailed description for each function is written within each function.

Before using the tool, python setup.py needs to be run.

	Usage: python3 -c 'from analysis import analize as an; run = an(<file>, <start step, <end step>); run.vibration(); value = run.msd(); run.rdf(<step>); run.response()'

	Example: python3 -c 'from analysis import analize as an; run = an("900K_1", 130000, 169000); run.vibration(); value = run.msd(); run.rdf(130000); run.response()'

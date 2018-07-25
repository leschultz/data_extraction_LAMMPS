General Documentation
=====================

Note: Python 3 and LAMMPS are required.
User must be in the directories noted below for functionality or add the folder to environment variables.

----------------------------

1. Located in bash folder. To generate input files, the following could be used (if invoked multiple times the same number of runs should be used):

	bash input_file_generator.sh <number of runs> <number of atoms> <melting temperature> <time steps at melt> <time steps of quench> <time steps final hold> <list of final temperatures without units>
	bash input_file_generator.sh 10 100 2000 1000000 33000000 36000000 900

2. Located in bash folder. To run lamps through each input file generated, the following could be used:

	bash lammps_looper.sh <lamps tool used>
	bash lammps_looper.sh lammps-daily

3. Located in python folder. To generate plots for data generated, the following could be used:

	python plots_over_time.py

4. Located in python folder. To generate displacement data, the folllowing could be used:

	python analysis.py

5. Located in python folder. To generate displacement plot, the following could be used:

	plot_analysis.py

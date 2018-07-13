TTT Generation Documentation
============================

Note: Python 2.7 is required.
User must be in the directories noted below for functionality or add the folder to environment variables.

----------------------------------------

1. Located in bash folder. To generate input files at a specified temperature in kelving, the following could be used:

	bash input_file_generator.sh <list of temperature without units>
	bash input_file_generator.sh 300 350 400 450 500 550 600 650 700 750 

2. Located in bash folder. To run lamps through each input file generated, the following could be used:

	bash lammps_looper.sh <lamps tool used> <list of temperature files generated>
	bash lammps_looper.sh lammps-daily 300.in 350.in 400.in 450.in 500.in 550.in 600.in 650.in 700.in 750.in

3. Located in python folder. To generate plots for data generated, teh following could be used:

	python data_analysis.py -n <list of temperatures without units>
	python data_analysis.py -n 300 350 400 450 500 550 600 650 700 750

General Documentation
=====================

Note: Python 3 and LAMMPS are required.
User must be in the directories noted below for functionality.

All calulations depend on the units used in LAMMPS. Ignore default units.

----------------------------

1. Located in bash folder. To generate input files, the following could be used (if invoked multiple times the same number of runs should be used):

	bash input_file_generator.sh <template file> <number of runs> <melting temperature> <time steps at melt> <time steps of quench> <time steps final hold> <list of final temperatures without units>
	bash input_file_generator.sh AlSm_template.in 10 2000 1000000 33000000 36000000 900

2. Located in bash folder. To run lamps through each input file generated, the following could be used:

	bash lammps_looper.sh <lamps tool used>
	bash lammps_looper.sh lmp_serial

3. Located in python folder. Data analysis script usage is described in the README.md in the python folder.

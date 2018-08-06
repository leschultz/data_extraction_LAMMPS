The python scripts used for analysing and plotting data are stored here.

	1. analysis.py gathers the displacement values for MD runs.
	2. plots_analysis.py plots the data from analysis.py.
	3. plots_over_time.py plots the system states from MD runs. 
	4. distance.py is a script that adds distances traversed between each step recorded.
	5. linearization.py linearizes the data for RMS displacement with respect to steps
	6. positions.py averages the runs from analysis.py for each temperature
	7. radial_distribution.py plots the LAMMPS output for the radial distributio function.
	8. setup.py creates needed directories and can delete previous run data.
	9. control.py is used to invoke other scripts.

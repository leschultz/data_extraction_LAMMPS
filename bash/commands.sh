#!/bin/bash

# -----Uncomment jobs to be run-----


# -----Sample AlSm runs to generate input files-----
#bash input_file_generator.sh AlSm_template.in 10 2000 100000 15000 36000 1500
#bash input_file_generator.sh AlSm_template.in 10 2000 100000 21000 36000 1300
#bash input_file_generator.sh AlSm_template.in 10 2000 100000 27000 36000 1100
#bash input_file_generator.sh AlSm_template.in 10 2000 100000 33000 36000 900

# -----Sample Si diamond cubic configuration runs to generate input files (Number of atoms has no effect on purpose)-----
#bash input_file_generator.sh Si_template.in 100 2000 100000 34000000 10000 300
#bash input_file_generator.sh Si_template.in 100 2000 100000 3400000 10000 300
#bash input_file_generator.sh Si_template.in 100 2000 100000 340000 10000 300
#bash input_file_generator.sh Si_template.in 100 2000 100000 34000 10000 300

# -----Loops for each input file and then used LAMMPS to compute-----
#bash lammps_looper.sh lmp_serial 

# -----Change the directory to where the python scripts are-----
#cd ../python

# -----Use the python scripts to analyze data-----
#python3 -c 'from control import control; control.analyze(1300, 0, 100); control.plot_analysis(180, 1000); control.plot_system(10)'


#!/bin/bash

# -----Uncomment jobs to be run-----


# -----Sample Si diamond cubic configuration runs to generate input files (Number of atoms has no effect on purpose)-----
bash input_file_generator.sh Si_template.in 100 2000 10000 34000 10000 300

# -----Loops for each input file and then used LAMMPS to compute-----
bash lammps_looper.sh lmp_serial 

# -----Change the directory to where the python scripts are-----
cd ../python

# -----Use the python scripts to analyze data-----
python3 -c 'from averages import avg; value = avg("300K", 10000+34000, 10000+34000+10000, 10000)'

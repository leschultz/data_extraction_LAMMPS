#!/bin/bash

# declare a name for this job (replace <jobname> with something more descriptive)
#$ -N propensity

# request the queue for this job
# currently only  morganshort.q is for serial jobs
#$ -q morganshort.q

# request 48 hours of wall time
#$ -l h_rt=48:00:00

# Specifies the interpreting shell for this job to be the Bash shell
#$ -S /bin/bash

# run the job from the directory of submission.Uncomment only if you don't want the defults.
#$ -cwd
# combine SGE standard output and error files
#$ -o $JOB_NAME.o$JOB_ID
#$ -e $JOB_NAME.e$JOB_ID
# transfer all your environment variables. Uncomment only if you don't want the defults
#$ -V

# Put the command to run one per line

## -----Uncomment jobs to be run-----


## -----Sample AlSm runs to generate input files-----
##bash input_file_generator.sh AlSm_template.in 10 100 2000 100000 15000 36000 1500
##bash input_file_generator.sh AlSm_template.in 10 100 2000 100000 21000 36000 1300
##bash input_file_generator.sh AlSm_template.in 10 100 2000 100000 27000 36000 1100
##bash input_file_generator.sh AlSm_template.in 10 100 2000 100000 33000 36000 900

## -----Sample Si diamond cubic configuration runs to generate input files-----
##bash input_file_generator.sh Si_template.in 100 85184 2000 100000 34000000 10000 300
##bash input_file_generator.sh Si_template.in 100 85184 2000 100000 3400000 10000 300
##bash input_file_generator.sh Si_template.in 100 85184 2000 100000 340000 10000 300
##bash input_file_generator.sh Si_template.in 100 85184 2000 100000 34000 10000 300

## -----Loops for each input file and then used LAMMPS to compute-----
##bash lammps_looper.sh lmp_turnbull

## -----Change the directory to where the python scripts are-----
##cd ../python

## -----Use the python scripts to analyze data-----
##python3 -c 'from control import control; control.analyze(1000); control.plot_analysis(180, 1000); control.plot_system()'

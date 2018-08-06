#!/bin/bash

## Declare a name for this job
#PBS -N propensity_for_motion
## Request the queue for this job (e.g. morganshort, morganeth, izabelaeth)
#PBS -q morgan2
## Request a total of 1 processor for this job (1 node and 1 processor per node)
#PBS -l nodes=1:ppn=1,pvmem=2000mb
## Request walltime. Max walltime for morganshort is 4:00:00
#PBS -l walltime=96:00:00
## These are PBS standard output and error files.  Uncomment only if you don't want the defaults.
#PBS -o output.$PBS_JOBID
#PBS -e error.$PBS_JOBID

## How many procs do I have?
NN=`cat $PBS_NODEFILE | wc -l`
echo "Processors received = "$NN
echo "script running on host `hostname`"

## cd into the directory where I typed qsub
cd $PBS_O_WORKDIR
echo "PBS_NODEFILE"
cat $PBS_NODEFILE

## Put the commands you want to run, one per line

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
##bash lammps_looper.sh lmp_bardeeneth

## -----Change the directory to where the python scripts are-----
##cd ../python

## -----Use the python scripts to analyze data-----
##python3 -c 'from control import control; control.analyze(1000,3000); control.plot_analysis(180, 1000); control.plot_system()'

#!/bin/bash

## Declare a name for this job
#PBS -N schultz
## Request the queue for this job (e.g. morganshort, morganeth, izabelaeth)
#PBS -q morganshort
## Request a total of 1 processor for this job (1 node and 1 processor per node)
#PBS -l nodes=1:ppn=1,pvmem=2000mb
## Request walltime. Max walltime for morganshort is 4:00:00
#PBS -l walltime=4:00:00
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
lmp_bardeeneth < 900.in
lmp_bardeeneth < 910.in
lmp_bardeeneth < 920.in
lmp_bardeeneth < 930.in
lmp_bardeeneth < 933.in
lmp_bardeeneth < 940.in
lmp_bardeeneth < 950.in
lmp_bardeeneth < 960.in
lmp_bardeeneth < 970.in
lmp_bardeeneth < 980.in
lmp_bardeeneth < 990.in
lmp_bardeeneth < 1000.in


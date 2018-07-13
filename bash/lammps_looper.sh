#!/bin/bash

cd ../lammps_runs/

program=$1

shift

for var in "$@"
do
	lammps-daily < $var 
done

#!/bin/bash

cd ../lammps_runs/

atom_number=$1
number_runs=$2

shift 2

for ((i=1;i<=$number_runs;i++))
do
	for var in "$@"
	do
		replaced=$(grep -l "replace_here" template.in | xargs sed "s/replace_here/$var/g; s/replace_seed/$RANDOM/g; s/replace_atom_number/$atom_number/g" > "$var"'K_'"$i.in")
	done
done

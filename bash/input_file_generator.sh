#!/bin/bash

cd ../lammps_runs/

atom_number=$1

shift

for var in "$@"
do
	replaced=$(grep -l "replace_here" template.in | xargs sed "s/replace_here/$var/g; s/replace_seed/$RANDOM/g; s/replace_atom_number/$atom_number/g" > "$var.in")
done

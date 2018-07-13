#!/bin/bash

cd ../lammps_runs/

for var in "$@"
do
	replaced=$(grep -l "replace_here" template.in | xargs sed "s/replace_here/$var/g" > "$var.in")
done

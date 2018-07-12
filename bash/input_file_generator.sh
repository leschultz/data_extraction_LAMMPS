#!/bin/bash

cd ../lammps_runs/

temperature=$1

replaced=$(grep -l "replace_here" template.in | xargs sed "s/replace_here/$temperature/g" > "$temperature.in")

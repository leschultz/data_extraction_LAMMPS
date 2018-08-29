#!/bin/bash

# Create the needed directories for LAMMPS
cd ../data/
mkdir -p dat
mkdir -p lammpstrj
mkdir -p rest
mkdir -p txt

# Change to inputfile directory
cd ../input_files/

program=$1

shift

for filename in *.in
do
	$program < $filename 
done

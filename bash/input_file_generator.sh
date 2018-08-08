#!/bin/bash

cd ../input_files

template_file=$1
number_runs=$2
temperature_melt=$3
hold_1=$4
hold_2=$5
hold_3=$6

shift 6 

for ((i=1;i<=$number_runs;i++))
do
	for var in "$@"
	do
		replaced=$(grep -l "replace_final_temperature" ../templates/$template_file | xargs sed "
		s/replace_final_temperature/$var/g;
	       	s/replace_seed/$RANDOM/g;
	       	s/replace_run/$i/g;
	       	s/replace_melt_temperature/$temperature_melt/g;
	       	s/replace_hold_1/$hold_1/g;
	       	s/replace_hold_2/$hold_2/g;
	       	s/replace_hold_3/$hold_3/g
		" > "$var"'K_'"$i.in")
	done
done

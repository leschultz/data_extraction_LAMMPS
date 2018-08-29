#!/bin/bash

cd ../input_files

template_file=$1
number_runs=$2
side_length=$3
hold_1=$4
hold_2=$5
hold_3=$6
timestep=$7
dumprate=$8
temperature0=$9

shift 9

# The innitial naming parameters
system_name=${template_file%_template.in}
name1='_boxside-'"$side_length"'_'
name2="$name1"'hold1-'"$hold_1"'_'
name3="$name2"'hold2-'"$hold_2"'_'
name4="$name3"'hold3-'"$hold_3"'_'
name5="$name4"'timestep-'"$timestep"'_'
name6="$name5"'dumprate-'"$dumprate"'_'
name7="$name6""$temperature0"'K-'
name8="$system_name""$name7"

# Replace any periods in the name with the letter p
filename=$(echo ${name8/./p})

for ((i=1;i<=$number_runs;i++))
do
	for var in "$@"
	do
                name="$filename""$var"'K_run'"$i"
		replaced=$(
                           grep -l "replace_final_temperature" ../templates/$template_file | xargs sed "
		s/replace_final_temperature/$var/g;
	       	s/replace_seed/$RANDOM/g;
	       	s/replace_run/$i/g;
                s/replace_side/$side_length/g;
	       	s/replace_initial_temperature/$temperature0/g;
	       	s/replace_hold_1/$hold_1/g;
	       	s/replace_hold_2/$hold_2/g;
	       	s/replace_hold_3/$hold_3/g;
                s/replace_timestep/$timestep/g;
                s/replace_dumprate/$dumprate/g;
                s/replace_system/$system_name/g;
                s/replace_filename/$name/g
		" > "$name"'.in')
	done
done

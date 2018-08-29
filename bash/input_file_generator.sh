#!/bin/bas

cd ../input_files

template_file=$1
number_runs=$2
side_length=$3
temperature0=$4
hold_1=$5
hold_2=$6
hold_3=$7

shift 7

# The innitial naming parameters
system_name=${template_file%_template.in}
name1='_boxside'"$side_length"'_'
name2="$name1"'hold1-'"$hold_1"'_'
name3="$name2"'hold2-'"$hold_2"'_'
name4="$name3"'hold3-'"$hold_3"'_'
namefinal="$name4""$temperature0"'K-'
inputfilename="$system_name""$namefinal"

for ((i=1;i<=$number_runs;i++))
do
	for var in "$@"
	do
                name="$inputfilename""$var"'K_run'"$i"
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
                s/replace_system/$system_name/g;
                s/replace_filename/$name/g
		" > "$name"'.in')
	done
done

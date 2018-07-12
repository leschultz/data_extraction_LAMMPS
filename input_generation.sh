#!/bin/bash

# Name of original stl file:
FileOld=$1

# Name of new stl file:
FileNew=$2

for location in ../Sessions/XML_Original/*.session
do
	cd ../../PythonTool/

	source ../BashTool/SessionReplaceNameIncrement.sh

	filename=$(echo "$location" | awk '{print $NF}' FS=/)

	grep "localhost:" "$filename" | sed "s/$FileOld/$FileNew/g" "$filename" > ../XML_Edited/"$name".session

done

printf "Session files where changed.\n"

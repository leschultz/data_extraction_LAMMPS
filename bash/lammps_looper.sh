#!/bin/bash

cd ../input_files/

program=$1

shift

for filename in *.in
do
	$program < $filename 
done

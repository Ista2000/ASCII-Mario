#!/bin/bash

echo > results.txt

for i in $( find *.py ); do
	echo -n $i >> results.txt; echo -n "  --  " >> results.txt 
    pylint $i | tail -2 >> results.txt
done
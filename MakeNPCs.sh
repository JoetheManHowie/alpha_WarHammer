#!/bin/bash

MAX=10

for((i = 0; i<MAX; i++)); do
	echo "$i"
	'./Make_a_warhammer_PC.py' 
done

./whatsNext.sh

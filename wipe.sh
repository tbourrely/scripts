#!/bin/bash
if [[ $# -eq 1 ]]; then
	if [[ -e $1  ]]; then
		echo -n "do you want to wipe $1 ? (y/n) : "
		read rep
		if [[ $rep == "y" || $rep == "Y" ]]; then
			echo "wipping $1"
			sudo dd if=/dev/zero of=$1
			for n in `seq 7`;
			do
				echo "pass $n"
				sudo dd if=/dev/random of=$1
			done
		fi
			
	else
		echo "path does not exist"
	fi
else
	echo "need 1 argument"
fi
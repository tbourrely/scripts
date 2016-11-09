#!/bin/bash
if [[ $# -eq 2 ]]; then
	dirt=$1
	dirn=$2
	if [[ -d ${dirt} ]]; then
		cmd="docker run -ti --rm -v ${dirt}:/${dirn} kali-linux-full /bin/bash"
		eval $cmd
	else
		echo "${dirt} n'est pas une repertoire valide"
	fi	
fi
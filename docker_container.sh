#!/bin/bash

fun(){
	if [[ -d $1 ]]; then
		cmd="docker run -ti --rm -v ${1}:/${2} kali-linux-full /bin/bash"
		eval $cmd
	else
		echo "${1} n'est pas une repertoire valide"
	fi
}

if [[ $# -eq 2 ]]; then
	dirt=$1
	dirn=$2
	fun $dirt $dirn
elif [[ $# -eq 1 ]]; then
	if [[ $1 == "systeme" ]]; then
		fun "/Volumes/TB_COURS/Cours/S3/Systeme/M3101-systeme-s3/Exercices/" "systeme"
	elif [[ $1 == "blackbox" ]]; then
		ip=$(ifconfig en0 | grep "inet " | cut -d ' ' -f 2)
		cmd="docker run -ti --rm --name blackbox -e DISPLAY=${ip}:0 -v /tmp/.X11-unix:/tmp/.X11-unix kali-linux-full /bin/bash"
		eval $cmd
	fi
fi
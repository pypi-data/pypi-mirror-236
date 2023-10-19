#!/usr/bin/env bash

usage="\
usage: $0 <files...>\n\
    -h         help\n\
"

echo=''

while getopts hetb: opt
do
    case $opt in
        h) echo -e "$usage"; exit;;
    esac
done

shift $((OPTIND-1))

IFS=$'\n'

touch .gitignore

for file in $*
do
    if [ -e "${file}" ]
    then
	ls -d ${file} | tee -a .gitignore
    fi
    uniq .gitignore > .gitignore.tmp
    mv .gitignore.tmp .gitignore
done



#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]
  then echo "No argument supplied: ./add-remove.sh username password 127.0.0.1 yes/no"
  exit 1
fi

username=$1
password=$2
address=$3
type=$4

if [[ "$4" == "yes" ]]; then
   python3 add-rtbh.py $1 $2 $3
elif [[ "$4" == "no" ]]; then
   python3 remove-rtbh.py $1 $2 $3
fi


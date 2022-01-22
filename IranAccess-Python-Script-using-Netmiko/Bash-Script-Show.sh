#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
  then echo "No argument supplied: ./showips.sh username password"
  exit 1
fi

username=$1
password=$2

python3 show-rtbh.py $1 $2


#!/bin/bash
if [ "$#" -lt 2 ]
then
  echo "usage wrong"
  exit 1
fi
echo $1
echo $2
curDir=$(pwd)
ls -all $curDir

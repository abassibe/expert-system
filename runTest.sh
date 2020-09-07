#!/bin/bash
FILES=./tests/*
for f in $FILES
do
  echo "Processing $f file..."
  cat $f
  echo '\n'
  python3 srcs/expertSystem.py $f
  echo '\n--------------\n'
done

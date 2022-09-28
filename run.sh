#!/bin/zsh

python3 puzzle.py $1 $2
cat output.txt
rm output.txt

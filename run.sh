#!/bin/zsh

python puzzle.py $1 $2
bat output.txt
rm output.txt

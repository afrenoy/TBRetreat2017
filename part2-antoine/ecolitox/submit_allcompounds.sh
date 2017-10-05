#!/usr/bin/env bash

for i in input/*; do
    ic50=$(./et0.py $i |sed 's/.*<pre>\(.*\)\\n<\/pre>.*/\1/g')
    echo $(basename $i): $ic50
done

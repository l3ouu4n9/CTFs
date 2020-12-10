#!/bin/bash

exec 2>/dev/null
python3 -u pow.py
valid_hash=$?
if [ $valid_hash -eq 1 ]; then
    echo 'There you go:'
    cat flag
else
    echo 'Wrong!!'
fi


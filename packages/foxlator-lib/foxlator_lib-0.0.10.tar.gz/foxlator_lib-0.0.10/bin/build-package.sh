#!/bin/bash

if [ -d ./dist ]; then
    echo "$ - found ./dist directory, removing"
    rm -rf ./dist
fi

python3.10 -m build 

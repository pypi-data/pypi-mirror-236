#!/bin/bash

echo "$ - installing python interpreter and necessary modules"
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-distutils python3.10-venv

echo "$ - installing pip"
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

python3.10 -m pip install --upgrade -r ./build-requirements.txt

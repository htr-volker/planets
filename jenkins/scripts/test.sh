#!/bin/bash

rm -rf venv
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
pip3 install pytest pytest-cov flask-testing

python3 -m pytest frontend
python3 -m pytest backend

deactivate

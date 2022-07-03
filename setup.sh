#!/usr/bin/env bash

if [[ ! `which python3` ]];then
    echo "Not installed python3"
    exit 1
fi

python3 -m venv .
source ./bin/activate
pip install -r requirements.txt
mkdir ./mysql_data
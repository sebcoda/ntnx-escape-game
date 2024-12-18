#!/bin/bash

cd ntnx-escape-game

source .venv/bin/activate

trap "" SIGINT

python main.py
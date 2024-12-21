#!/bin/bash

cd ntnx-escape-game

source .venv/bin/activate

trap "" INT TSTP #Ctrl + c / Ctrl + z
export IGNOREEOF=42 # Ctrl + d

python main.py

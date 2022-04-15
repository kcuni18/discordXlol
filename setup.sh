#!/bin/bash

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
./init.sh
python -m pip install -r dependencies_py.txt

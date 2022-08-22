#!/bin/bash

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
./scripts/init.sh
python -m pip install -r requirements.txt

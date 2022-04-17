@echo off

python -m pip install poetry
python -m poetry install

python src\setup.py

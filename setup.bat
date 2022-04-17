@echo off

if NOT EXIST .venv (
	python -m venv .venv
)
CALL init.bat
python -m pip install -r requirements.txt

python src\setup.py

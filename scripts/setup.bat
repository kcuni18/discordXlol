@echo off

if NOT EXIST .venv (
	python -m venv .venv
)
CALL scripts\init.bat
python -m pip install -r requirements.txt

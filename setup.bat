@echo off

if NOT EXIST .venv (
	python -m venv .venv
)
CALL init.bat
python -m pip install -r dependencies_py.txt

cd c_db_py
CALL build.bat
python setup.py install
cd ..

@echo off

if NOT EXIST .venv (
	python -m venv .venv
)
CALL init.bat
python -m pip install -r dependencies_py.txt

cd py_c_db
CALL build.bat
python setup.py install
cd ..

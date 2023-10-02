@echo off
setlocal

rem Set the path to your virtual environment activate script
set VENV_PATH=your_venv_path\Scripts\activate

rem Set the path to your Python script
set SCRIPT_PATH=your_script_path
set SCRIPT_NAME=your_script_name.py

rem Activate the virtual environment
call "%VENV_PATH%"

rem Change to the script directory
cd "%SCRIPT_PATH%"

rem Execute your Python script
python "%SCRIPT_NAME%"

rem Deactivate the virtual environment (optional)
deactivate

endlocal
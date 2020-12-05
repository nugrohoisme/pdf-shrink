@echo off

set DIR=%~dp0

CALL %DIR%\venv\Scripts\activate
python3 %DIR%\gui.py
CALL deactivate
echo.
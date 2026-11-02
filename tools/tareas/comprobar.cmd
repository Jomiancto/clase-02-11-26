@echo off
call E:\cmder\vendor\init.bat
cd /d "%~dp0..\.."
.venv\Scripts\python.exe tools\ejecutar.py .venv\Scripts\python.exe manage.py check

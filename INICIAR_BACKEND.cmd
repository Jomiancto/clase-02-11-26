@echo off
setlocal
cd /d "%~dp0"
if not defined CMDER_ROOT (
  echo Abrir Cmder y ejecutar este archivo desde una sesion cmd.
  exit /b 1
)
if not defined ConEmuPID (
  echo Se requiere una consola Cmder activa.
  exit /b 1
)
if not exist .venv\Scripts\python.exe (
  echo Falta .venv. Consultar README.md antes de instalar.
  exit /b 1
)
set "PUERTO_BACKEND=8000"
if not "%~1"=="" set "PUERTO_BACKEND=%~1"
echo(%PUERTO_BACKEND%| findstr /r /x "[0-9][0-9]*" >nul
if errorlevel 1 exit /b 1
call .venv\Scripts\activate.bat
.venv\Scripts\python.exe tools\ejecutar.py .venv\Scripts\python.exe tools\mariadb_local.py
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe tools\ejecutar.py .venv\Scripts\python.exe manage.py check
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe tools\ejecutar.py .venv\Scripts\python.exe manage.py migrate --check
if errorlevel 1 (
  echo Hay migraciones pendientes. Revisar el plan antes de aplicarlas.
  exit /b 1
)
.venv\Scripts\python.exe tools\ejecutar.py .venv\Scripts\python.exe tools\puerto.py %PUERTO_BACKEND%
if errorlevel 1 exit /b 1
echo Servidor local: http://127.0.0.1:%PUERTO_BACKEND%/api/
echo Detener Django con Ctrl+C. MariaDB permanece activa.
.venv\Scripts\python.exe tools\ejecutar.py .venv\Scripts\python.exe manage.py runserver 127.0.0.1:%PUERTO_BACKEND% --noreload
exit /b %errorlevel%

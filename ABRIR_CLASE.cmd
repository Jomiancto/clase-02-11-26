@echo off
cd /d "%~dp0"
if not defined CMDER_ROOT exit /b 1
call E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir "%CD%\.local\editor-data" --extensions-dir "%CD%\.local\editor-extensions" --reuse-window "%CD%" "bruno\03 Crear producto.bru" "pedidos_app\serializers.py" "sql\verificar_create.sql"
.venv\Scripts\python.exe tools\abrir_cmder.py 8000

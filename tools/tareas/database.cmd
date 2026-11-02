@echo off
call E:\cmder\vendor\init.bat
cd /d "%~dp0..\.."
call E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir "%CD%\.local\editor-data" --extensions-dir "%CD%\.local\editor-extensions" --reuse-window sql\verificar_create.sql

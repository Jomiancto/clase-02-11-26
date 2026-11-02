# Comandos Cmder — 2 de noviembre de 2026

Directorio de tareas: E:/cmder/clase-02-11-26.
Cada proceso verifica CMDER_ROOT y ConEmuPID. Despacho con Cmder.exe /START y
/X -NoSingle -run @archivo.task. Las fases usan cmd.exe /d /k, vendor/init.bat,
cd /d y tools/ejecutar.py. Los scripts exactos se incluyen abajo.
Logs completos locales: .local/*.log y .local/comandos.jsonl.
Las lecturas y ediciones mediante herramientas de archivos no son comandos de consola.
Una lectura inicial de la habilidad Windows se hizo mediante PowerShell;
Git, Django, MariaDB y la preparacion del editor se ejecutaron mediante Cmder.

## Errores y soluciones

- 03_diagnostico: UnicodeEncodeError al imprimir netstat con cp1252.
  Corregido tools/ejecutar.py a UTF-8 con sustitucion; repetido en 04_editor.
- 06_servidor: ModuleNotFoundError django; el hijo resolvia Python global.
  INICIAR_BACKEND.cmd usa ahora .venv/Scripts/python.exe explicitamente.
  Segundo arranque: 07_servidor en 8000.
- Bruno 6 en VS Code 1.88.1 no activa por crypto.subtle. Tres extensiones DB
  chocan. Se preparo un editor independiente actual con extensiones aisladas.

- 09_editor_actual: ZIP actual usa directorio de version; deteccion corregida.
- 10_editor_actual: nombre de extension Python Envs sin sufijo win32-x64; corregido.
- 12_verificacion: diff --check detecto linea vacia al final del historial; generador ajustado.

## Comandos finalizados

### 1. 2026-11-02T10:35:48

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 18708.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git -C E:\cmder\Unidad2 status --short --branch
```

Resultado: codigo 0.

### 2. 2026-11-02T10:35:49

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 18708.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git -C E:\cmder\Unidad2 log -3 --oneline
```

Resultado: codigo 0.

### 3. 2026-11-02T10:35:49

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 18708.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git -C E:\cmder\Unidad2 remote -v
```

Resultado: codigo 0.

### 4. 2026-11-02T10:35:49

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 18708.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git ls-remote https://github.com/Jomiancto/Unidad2.git
```

Resultado: codigo 0.

### 5. 2026-11-02T10:35:52

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 18708.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git ls-remote https://github.com/Jomiancto/clase-02-11-26.git
```

Resultado: codigo 0.

### 6. 2026-11-02T10:35:53

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 18708.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git ls-remote https://github.com/enriquepalaciosc/pbe-2026_u2_proyecto1.git
```

Resultado: codigo 0.

### 7. 2026-11-02T10:36:15

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
"C:\Program Files\Python312\python.exe" .local\copiar.py
```

Resultado: codigo 0.

### 8. 2026-11-02T10:36:15

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git init -b main
```

Resultado: codigo 0.

### 9. 2026-11-02T10:36:15

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git remote add origin https://github.com/Jomiancto/clase-02-11-26.git
```

Resultado: codigo 0.

### 10. 2026-11-02T10:36:16

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
"C:\Program Files\Python312\python.exe" -m venv .venv
```

Resultado: codigo 0.

### 11. 2026-11-02T10:36:34

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Comprobar/instalar dependencias del entorno independiente.

```bat
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Resultado: codigo 0.

### 12. 2026-11-02T10:37:10

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Comprobar/instalar dependencias del entorno independiente.

```bat
.venv\Scripts\python.exe -m pip check
```

Resultado: codigo 0.

### 13. 2026-11-02T10:37:12

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\mariadb_local.py
```

Resultado: codigo 0.

### 14. 2026-11-02T10:37:17

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe manage.py check
```

Resultado: codigo 0.

### 15. 2026-11-02T10:37:19

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Inspeccionar migraciones sin modificar el esquema.

```bat
.venv\Scripts\python.exe manage.py showmigrations
```

Resultado: codigo 0.

### 16. 2026-11-02T10:37:22

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Inspeccionar migraciones sin modificar el esquema.

```bat
.venv\Scripts\python.exe manage.py migrate --plan
```

Resultado: codigo 0.

### 17. 2026-11-02T10:37:24

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Inspeccionar migraciones sin modificar el esquema.

```bat
.venv\Scripts\python.exe manage.py migrate --check
```

Resultado: codigo 0.

### 18. 2026-11-02T10:37:26

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17228.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\inspeccionar_bd.py --despues
```

Resultado: codigo 0.

### 19. 2026-11-02T10:37:58

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17036.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\diagnostico.py
```

Resultado: codigo 0.

### 20. 2026-11-02T10:38:02

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17036.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
"C:\Program Files\Microsoft VS Code\bin\code.cmd" --list-extensions --show-versions
```

Resultado: codigo 0.

### 21. 2026-11-02T10:38:03

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17036.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
"C:\Program Files\Microsoft VS Code\bin\code.cmd" --reuse-window E:\cmder\clase-02-11-26
```

Resultado: codigo 0.

### 22. 2026-11-02T10:38:18

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 936.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe manage.py check
```

Resultado: codigo 0.

### 23. 2026-11-02T10:38:20

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 936.

Objetivo: Inspeccionar migraciones sin modificar el esquema.

```bat
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Resultado: codigo 0.

### 24. 2026-11-02T10:38:23

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 936.

Objetivo: Inspeccionar migraciones sin modificar el esquema.

```bat
.venv\Scripts\python.exe manage.py migrate --check
```

Resultado: codigo 0.

### 25. 2026-11-02T10:38:25

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 936.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\respaldo_bd.py
```

Resultado: codigo 0.

### 26. 2026-11-02T10:38:51

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16612.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
python tools\mariadb_local.py
```

Resultado: codigo 0.

### 27. 2026-11-02T10:38:51

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16612.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
python manage.py check
```

Resultado: codigo 1.

Error: consultar soluciones anteriores y log local de la fase.

### 28. 2026-11-02T10:38:51

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16612.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
cmd.exe /d /c INICIAR_BACKEND.cmd 8000
```

Resultado: codigo 1.

Error: consultar soluciones anteriores y log local de la fase.

### 29. 2026-11-02T10:39:07

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16648.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\mariadb_local.py
```

Resultado: codigo 0.

### 30. 2026-11-02T10:39:07

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16648.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe manage.py check
```

Resultado: codigo 0.

### 31. 2026-11-02T10:39:10

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16648.

Objetivo: Inspeccionar migraciones sin modificar el esquema.

```bat
.venv\Scripts\python.exe manage.py migrate --check
```

Resultado: codigo 0.

### 32. 2026-11-02T10:39:12

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 16648.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\puerto.py 8000
```

Resultado: codigo 0.

### 33. 2026-11-02T10:40:16

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 20044.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\probar_create.py
```

Resultado: codigo 0.

### 34. 2026-11-02T10:41:17

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 3692.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\preparar_editor.py
```

Resultado: codigo 1.

Error: consultar soluciones anteriores y log local de la fase.

### 35. 2026-11-02T10:44:31

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19772.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\preparar_editor.py
```

Resultado: codigo 1.

Error: consultar soluciones anteriores y log local de la fase.

### 36. 2026-11-02T10:46:12

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 8792.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\preparar_editor.py
```

Resultado: codigo 0.

### 37. 2026-11-02T10:46:13

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 8792.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir E:\cmder\clase-02-11-26\.local\editor-data --extensions-dir E:\cmder\clase-02-11-26\.local\editor-extensions --new-window E:\cmder\clase-02-11-26
```

Resultado: codigo 0.

### 38. 2026-11-02T10:47:59

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\verificar_origen.py
```

Resultado: codigo 0.

### 39. 2026-11-02T10:47:59

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\verificar_http.py 8000
```

Resultado: codigo 0.

### 40. 2026-11-02T10:48:00

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\verificar_remoto.py
```

Resultado: codigo 0.

### 41. 2026-11-02T10:48:00

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git -C E:\cmder\Unidad2 status --short --branch
```

Resultado: codigo 0.

### 42. 2026-11-02T10:48:01

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\documentar_comandos.py
```

Resultado: codigo 0.

### 43. 2026-11-02T10:48:01

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git add -- .
```

Resultado: codigo 0.

### 44. 2026-11-02T10:48:02

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19124.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\revisar_publicacion.py
```

Resultado: codigo 1.

Error: consultar soluciones anteriores y log local de la fase.

### 45. 2026-11-02T10:48:39

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\documentar_comandos.py
```

Resultado: codigo 0.

### 46. 2026-11-02T10:48:39

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git add -- .
```

Resultado: codigo 0.

### 47. 2026-11-02T10:48:40

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\revisar_publicacion.py
```

Resultado: codigo 0.

### 48. 2026-11-02T10:48:47

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git diff --cached --stat
```

Resultado: codigo 0.

### 49. 2026-11-02T10:48:47

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git -c commit.gpgsign=false commit -m "Recuperar backend y completar CREATE con DRF, Bruno y Cmder"
```

Resultado: codigo 0.

### 50. 2026-11-02T10:50:03

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 21000.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\verificar_local_final.py
```

Resultado: codigo 0.

### 51. 2026-11-02T10:50:05

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 21000.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe tools\documentar_comandos.py
```

Resultado: codigo 0.

### 52. 2026-11-02T10:50:27

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 19840.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir E:\cmder\clase-02-11-26\.local\editor-data --extensions-dir E:\cmder\clase-02-11-26\.local\editor-extensions --reuse-window E:\cmder\clase-02-11-26\pedidos_app\serializers.py E:\cmder\clase-02-11-26\sql\verificar_create.sql "E:\cmder\clase-02-11-26\bruno\03 Crear producto.bru"
```

Resultado: codigo 0.

### 53. 2026-11-02T10:48:48

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git push -u origin main
```

Resultado: codigo 0.

### 54. 2026-11-02T10:50:49

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git log -1 --oneline
```

Resultado: codigo 0.

### 55. 2026-11-02T10:50:50

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 17580.

Objetivo: Revisar/preparar/publicar repositorio oficial; fuentes antiguas solo lectura.

```bat
git ls-remote origin refs/heads/main
```

Resultado: codigo 0.

### 56. 2026-11-02T10:57:38

Directorio: E:\cmder\clase-02-11-26. ConEmuPID: 22428.

Objetivo: Preparar o comprobar el componente indicado con resultado real registrado.

```bat
.venv\Scripts\python.exe .local\verificar_bruno.py
```

Resultado: codigo 0.

## Procesos activos y comando interrumpido

03_diagnostico ejecuto .venv/Scripts/python.exe .local/diagnostico.py;
no termino su registro por UnicodeEncodeError; la repeticion si esta registrada.

07_servidor: cmd.exe /d /c INICIAR_BACKEND.cmd 8000 permanece ejecutandose.
Ejecuta .venv/Scripts/python.exe manage.py runserver 127.0.0.1:8000 --noreload
mediante tools/ejecutar.py. No tiene codigo de salida final mientras sigue activo.
El iniciador ejecuta cd /d "%~dp0" y call .venv/Scripts/activate.bat.
Los check previos estan registrados y HTTP se verifico con tools/probar_create.py.

## Despacho de fases realmente ejecutadas

Archivo local: .local/01_repos.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\01_repos.log 2>&1
set "RESULT=%errorlevel%"
> .local\01_repos.exit echo %RESULT%
type .local\01_repos.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git -C E:\cmder\Unidad2 status --short --branch
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git -C E:\cmder\Unidad2 log -3 --oneline
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git -C E:\cmder\Unidad2 remote -v
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git ls-remote https://github.com/Jomiancto/Unidad2.git
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git ls-remote https://github.com/Jomiancto/clase-02-11-26.git
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git ls-remote https://github.com/enriquepalaciosc/pbe-2026_u2_proyecto1.git
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/02_copia.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\02_copia.log 2>&1
set "RESULT=%errorlevel%"
> .local\02_copia.exit echo %RESULT%
type .local\02_copia.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py "C:\Program Files\Python312\python.exe" .local\copiar.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git init -b main
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git remote add origin https://github.com/Jomiancto/clase-02-11-26.git
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py "C:\Program Files\Python312\python.exe" -m venv .venv
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe -m pip check
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\mariadb_local.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py check
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py showmigrations
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py migrate --plan
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py migrate --check
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\inspeccionar_bd.py --despues
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/03_diagnostico.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\03_diagnostico.log 2>&1
set "RESULT=%errorlevel%"
> .local\03_diagnostico.exit echo %RESULT%
type .local\03_diagnostico.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\diagnostico.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py "C:\Program Files\Microsoft VS Code\bin\code.cmd" --list-extensions --show-versions
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py "C:\Program Files\Microsoft VS Code\bin\code.cmd" --reuse-window E:\cmder\clase-02-11-26
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/04_editor.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\04_editor.log 2>&1
set "RESULT=%errorlevel%"
> .local\04_editor.exit echo %RESULT%
type .local\04_editor.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\diagnostico.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py "C:\Program Files\Microsoft VS Code\bin\code.cmd" --list-extensions --show-versions
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py "C:\Program Files\Microsoft VS Code\bin\code.cmd" --reuse-window E:\cmder\clase-02-11-26
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/05_validar.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\05_validar.log 2>&1
set "RESULT=%errorlevel%"
> .local\05_validar.exit echo %RESULT%
type .local\05_validar.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py check
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py makemigrations --check --dry-run
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe manage.py migrate --check
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\respaldo_bd.py
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/06_servidor.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\06_servidor.log 2>&1
set "RESULT=%errorlevel%"
> .local\06_servidor.exit echo %RESULT%
type .local\06_servidor.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py cmd.exe /d /c INICIAR_BACKEND.cmd 8000
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/07_servidor.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\07_servidor.log 2>&1
set "RESULT=%errorlevel%"
> .local\07_servidor.exit echo %RESULT%
type .local\07_servidor.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py cmd.exe /d /c INICIAR_BACKEND.cmd 8000
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/08_pruebas.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\08_pruebas.log 2>&1
set "RESULT=%errorlevel%"
> .local\08_pruebas.exit echo %RESULT%
type .local\08_pruebas.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\probar_create.py
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/09_editor_actual.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\09_editor_actual.log 2>&1
set "RESULT=%errorlevel%"
> .local\09_editor_actual.exit echo %RESULT%
type .local\09_editor_actual.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\preparar_editor.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir E:\cmder\clase-02-11-26\.local\editor-data --extensions-dir E:\cmder\clase-02-11-26\.local\editor-extensions --new-window E:\cmder\clase-02-11-26
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/10_editor_actual.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\10_editor_actual.log 2>&1
set "RESULT=%errorlevel%"
> .local\10_editor_actual.exit echo %RESULT%
type .local\10_editor_actual.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\preparar_editor.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir E:\cmder\clase-02-11-26\.local\editor-data --extensions-dir E:\cmder\clase-02-11-26\.local\editor-extensions --new-window E:\cmder\clase-02-11-26
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/11_editor_actual.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\11_editor_actual.log 2>&1
set "RESULT=%errorlevel%"
> .local\11_editor_actual.exit echo %RESULT%
type .local\11_editor_actual.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\preparar_editor.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir E:\cmder\clase-02-11-26\.local\editor-data --extensions-dir E:\cmder\clase-02-11-26\.local\editor-extensions --new-window E:\cmder\clase-02-11-26
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/12_verificacion.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\12_verificacion.log 2>&1
set "RESULT=%errorlevel%"
> .local\12_verificacion.exit echo %RESULT%
type .local\12_verificacion.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\verificar_origen.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\verificar_http.py 8000
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\verificar_remoto.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git -C E:\cmder\Unidad2 status --short --branch
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\documentar_comandos.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git add -- .
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\revisar_publicacion.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git diff --cached --stat
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/13_publicacion.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\13_publicacion.log 2>&1
set "RESULT=%errorlevel%"
> .local\13_publicacion.exit echo %RESULT%
type .local\13_publicacion.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\documentar_comandos.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git add -- .
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\revisar_publicacion.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git diff --cached --stat
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git -c commit.gpgsign=false commit -m "Recuperar backend y completar CREATE con DRF, Bruno y Cmder"
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git push -u origin main
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git log -1 --oneline
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git ls-remote origin refs/heads/main
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/14_estado_local.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\14_estado_local.log 2>&1
set "RESULT=%errorlevel%"
> .local\14_estado_local.exit echo %RESULT%
type .local\14_estado_local.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\verificar_local_final.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\documentar_comandos.py
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/15_pestanas.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\15_pestanas.log 2>&1
set "RESULT=%errorlevel%"
> .local\15_pestanas.exit echo %RESULT%
type .local\15_pestanas.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py E:\cmder\opt\vscode-backend\bin\code.cmd --user-data-dir E:\cmder\clase-02-11-26\.local\editor-data --extensions-dir E:\cmder\clase-02-11-26\.local\editor-extensions --reuse-window E:\cmder\clase-02-11-26\pedidos_app\serializers.py E:\cmder\clase-02-11-26\sql\verificar_create.sql "E:\cmder\clase-02-11-26\bruno\03 Crear producto.bru"
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/16_bruno_sql.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\16_bruno_sql.log 2>&1
set "RESULT=%errorlevel%"
> .local\16_bruno_sql.exit echo %RESULT%
type .local\16_bruno_sql.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe .local\verificar_bruno.py
if errorlevel 1 exit /b 1
exit /b 0
```

Archivo local: .local/17_cierre.cmd

```bat
@echo off
call E:\cmder\vendor\init.bat
cd /d E:\cmder\clase-02-11-26
call :work > .local\17_cierre.log 2>&1
set "RESULT=%errorlevel%"
> .local\17_cierre.exit echo %RESULT%
type .local\17_cierre.log
exit /b %RESULT%
:work
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\documentar_comandos.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git add -- README.md INFORME_BACKEND.md COMANDOS_CMDER.md tools/documentar_comandos.py bruno/environments/Local.bru
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py .venv\Scripts\python.exe tools\revisar_publicacion.py
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git -c commit.gpgsign=false commit -m "Documentar prueba visual Bruno MariaDB y entorno VS Code"
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git push origin main
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git log -1 --oneline
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git ls-remote origin refs/heads/main
if errorlevel 1 exit /b 1
"C:\Program Files\Python312\python.exe" tools\ejecutar.py git status --short --branch
if errorlevel 1 exit /b 1
exit /b 0
```

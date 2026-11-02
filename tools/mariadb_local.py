"""Inicia unicamente la instancia portatil verificada, sin inicializar datos."""
import configparser
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

raiz = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(raiz))
from u2_proyecto1.entorno import cargar_entorno
cargar_entorno(raiz / '.env')
host = os.environ.get('DB_HOST', '127.0.0.1')
puerto = int(os.environ.get('DB_PORT', '3306'))
if host not in ('127.0.0.1', 'localhost') or puerto != 3306:
    raise SystemExit('Configuracion distinta de la instancia local verificada; revisar manualmente.')


def escuchando():
    try:
        with socket.create_connection((host, puerto), timeout=1):
            return True
    except OSError:
        return False


if escuchando():
    print('Puerto MariaDB 3306 activo; se comprobara identidad y conexion con Django.')
    raise SystemExit(0)
servidor = Path(r'E:\MariaDB\mariadb-12.3.2-winx64\mariadb-12.3.2-winx64')
ejecutable = servidor / 'bin' / 'mysqld.exe'
configuracion = servidor / 'data' / 'my.ini'
if not ejecutable.is_file() or not configuracion.is_file() or not (servidor / 'data' / 'mysql').is_dir():
    raise SystemExit('No existe la instancia inicializada. No se creara otra.')
config = configparser.ConfigParser()
config.read(configuracion)
if Path(config['mysqld']['datadir']).resolve() != (servidor / 'data').resolve():
    raise SystemExit('my.ini apunta a otro directorio de datos; revisar manualmente.')
procesos = subprocess.check_output(['tasklist', '/fo', 'csv', '/nh']).lower()
if b'"mysqld.exe"' in procesos or b'"mariadbd.exe"' in procesos:
    raise SystemExit('Ya hay un proceso DB sin responder en 3306; no se inicia otro.')
local = raiz / '.local'
local.mkdir(exist_ok=True)
with (local / 'mariadb.log').open('ab') as log:
    proceso = subprocess.Popen([str(ejecutable), f'--defaults-file={configuracion}',
                               '--bind-address=127.0.0.1', '--port=3306', '--console'],
                              cwd=servidor, stdout=log, stderr=log,
                              creationflags=subprocess.CREATE_NO_WINDOW)
for intento in range(30):
    if escuchando():
        print('Instancia MariaDB local iniciada; PID', proceso.pid)
        break
    if proceso.poll() is not None:
        raise SystemExit('MariaDB finalizo; revisar .local/mariadb.log.')
    time.sleep(0.5)
else:
    raise SystemExit('MariaDB no responde; revisar .local/mariadb.log.')

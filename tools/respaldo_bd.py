"""Respaldo local previo a migraciones; contraseña solo en entorno del proceso hijo."""
import datetime
import os
from pathlib import Path
import subprocess
import sys

raiz = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(raiz))
from u2_proyecto1.entorno import cargar_entorno
cargar_entorno(raiz / '.env')
directorio = raiz / '.local' / 'respaldos'
directorio.mkdir(parents=True, exist_ok=True)
destino = directorio / ('u2_p1_bd_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.sql')
dump = Path(r'E:\MariaDB\mariadb-12.3.2-winx64\mariadb-12.3.2-winx64\bin\mariadb-dump.exe')
if not dump.is_file():
    raise SystemExit('No existe mariadb-dump; no se migrara sin respaldo.')
entorno = os.environ.copy()
entorno['MYSQL_PWD'] = entorno.get('DB_PASSWORD', '')
subprocess.run([str(dump), '--host=' + entorno['DB_HOST'], '--port=' + entorno['DB_PORT'],
                '--user=' + entorno['DB_USER'], '--single-transaction',
                '--result-file=' + str(destino), entorno['DB_NAME']], env=entorno, check=True)
if destino.stat().st_size == 0:
    raise SystemExit('Respaldo vacio; revisar antes de migrar.')
print('Respaldo local creado, no versionado; bytes:', destino.stat().st_size)

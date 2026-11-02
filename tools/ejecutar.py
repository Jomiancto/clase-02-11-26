"""Registra comandos ejecutados por tareas de Cmder; nunca recibe secretos."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

raiz = Path(__file__).resolve().parent.parent
local = raiz / '.local'
local.mkdir(exist_ok=True)
if not os.environ.get('ConEmuPID') or not os.environ.get('CMDER_ROOT'):
    raise SystemExit('Esta tarea debe ejecutarse dentro de Cmder.')
comando = sys.argv[1:]
if not comando:
    raise SystemExit('Falta comando')
texto = subprocess.list2cmdline(comando)
print('\nCMDER> ' + texto, flush=True)
registro = {
    'fecha': datetime.datetime.now().isoformat(timespec='seconds'),
    'directorio': str(Path.cwd()), 'comando': texto,
    'cmder': os.environ['CMDER_ROOT'], 'conemu_pid': os.environ['ConEmuPID'],
}
proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
salida = []
for linea in iter(proceso.stdout.readline, b''):
    decodificada = linea.decode('utf-8', errors='replace')
    salida.append(decodificada)
    print(decodificada, end='', flush=True)
codigo = proceso.wait()
registro.update(codigo=codigo, salida=''.join(salida))
with (local / 'comandos.jsonl').open('a', encoding='utf-8') as archivo:
    archivo.write(json.dumps(registro, ensure_ascii=False) + '\n')
print('Resultado:', codigo, flush=True)
sys.exit(codigo)

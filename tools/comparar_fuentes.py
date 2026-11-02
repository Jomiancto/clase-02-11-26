"""Verifica identidad de archivos originales, admitiendo solo newline final de texto."""
import hashlib
import json
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
origen = json.loads((raiz / 'ORIGEN_PROFESOR.json').read_text(encoding='utf-8'))
for entrada in origen['files']:
    if entrada['adapted']:
        print('ADAPTADO:', entrada['path'], '(entorno y credenciales)')
        continue
    datos = (raiz / entrada['path']).read_bytes().replace(b'\r\n', b'\n')
    opciones = [datos, datos.rstrip(b'\n'), datos.rstrip(b'\n') + b'\n']
    def blob(valor):
        return hashlib.sha1(b'blob ' + str(len(valor)).encode() + b'\0' + valor).hexdigest()
    if not any(blob(opcion) == entrada['git_blob'] for opcion in opciones):
        raise SystemExit('Diferencia no autorizada: ' + entrada['path'])
    print('IDENTICO:', entrada['path'])
print('Fuentes originales verificadas; solo settings.py adaptado.')

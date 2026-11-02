"""Revisa el contenido preparado para Git sin revelar valores sensibles."""
import os
from pathlib import Path
import re
import subprocess
import sys

raiz = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(raiz))
from u2_proyecto1.entorno import cargar_entorno
cargar_entorno(raiz / '.env')
archivos = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z']).decode().split('\0')
archivos = [p for p in archivos if p]
if not archivos:
    raise SystemExit('No hay archivos preparados; revisar antes de publicar.')
prohibidos = re.compile(r'(^|/)(\.venv|__pycache__|\.local|\.idea)(/|$)|(^|/)\.env($|\.)|\.(pyc|sqlite3|log|pem|key)$|(^|/)(my\.ini|my\.cnf|local_settings\.py)$')
secretos = [v.encode() for k in ('SECRET_KEY', 'DB_PASSWORD') if len(v := os.environ.get(k, '')) >= 4]
tokens = re.compile(rb'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----')
for nombre in archivos:
    if nombre != '.env.example' and prohibidos.search(nombre):
        raise SystemExit('Archivo privado/innecesario preparado: ' + nombre)
    contenido = subprocess.check_output(['git', 'show', ':' + nombre])
    if any(v in contenido for v in secretos) or tokens.search(contenido) or (b'django' + b'-insecure-') in contenido:
        raise SystemExit('Posible secreto en ' + nombre + '; no se imprime su contenido.')
    if nombre.endswith('.py'):
        compile(contenido, nombre, 'exec')
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
print('Revision correcta:', len(archivos), 'archivos, sin credenciales locales, tokens detectados ni archivos prohibidos.')
print('Revision de patrones y valores locales; no es una garantia universal de ausencia de secretos.')

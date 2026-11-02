"""Conserva la credencial propia ya existente sin imprimirla ni copiar la del profesor."""
import ast
import json
from pathlib import Path
import secrets

raiz = Path(__file__).resolve().parent.parent
archivo = raiz / '.env'
if archivo.exists():
    print('.env existente conservado; no se sobrescribe.')
else:
    privado = Path(r'E:\cmder\u2_proyecto1\u2_proyecto1\local_settings.py')
    if not privado.is_file():
        raise SystemExit('Falta configuracion local anterior; completar .env manualmente.')
    arbol = ast.parse(privado.read_text(encoding='utf-8'))
    valores = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name):
            if nodo.targets[0].id == 'DB_PASSWORD':
                valores['DB_PASSWORD'] = ast.literal_eval(nodo.value)
    if 'DB_PASSWORD' not in valores:
        raise SystemExit('No se encontro credencial local; no se usa la del profesor.')
    datos = {'SECRET_KEY': secrets.token_urlsafe(64), 'DB_NAME': 'u2_p1_bd',
             'DB_USER': 'root', 'DB_PASSWORD': valores['DB_PASSWORD'],
             'DB_HOST': '127.0.0.1', 'DB_PORT': '3306'}
    archivo.write_text(''.join(f'{k}={json.dumps(v)}\n' for k, v in datos.items()), encoding='utf-8')
    print('.env privado creado con clave nueva y credencial propia conservada; valores omitidos.')

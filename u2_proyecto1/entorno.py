"""Carga opcional de .env local; el entorno del proceso tiene prioridad."""
import json
import os


def cargar_entorno(archivo):
    if not archivo.is_file():
        return
    for numero, linea in enumerate(archivo.read_text(encoding='utf-8').splitlines(), 1):
        linea = linea.strip()
        if not linea or linea.startswith('#'):
            continue
        nombre, separador, valor = linea.partition('=')
        if not separador or nombre.strip() not in {
            'SECRET_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT'
        }:
            raise ValueError(f'Entrada .env invalida en linea {numero}')
        valor = valor.strip()
        if valor.startswith('"'):
            valor = json.loads(valor)
        os.environ.setdefault(nombre.strip(), valor)

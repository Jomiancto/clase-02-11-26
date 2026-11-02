"""Comprueba READ, API anterior y CREATE sin insertar/modificar/borrar filas."""
import hashlib
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import uuid

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u2_proyecto1.settings')
import django
django.setup()
from django.db import connection
from pedidos_app.models import Cliente
from pedidos_app.serializers import ClienteSerializer
from pedidos_app.views import ClienteView
from rest_framework.test import APIRequestFactory

base = 'http://127.0.0.1:' + (sys.argv[1] if len(sys.argv) > 1 else '8000')


def snapshot():
    result = {}
    with connection.cursor() as cursor:
        for table in sorted(connection.introspection.table_names()):
            if not table.startswith(('pedidos_app_', 'productos_app_')):
                continue
            cursor.execute('SELECT * FROM ' + connection.ops.quote_name(table) + ' ORDER BY id')
            rows = cursor.fetchall()
            result[table] = (len(rows), hashlib.sha256(json.dumps(rows, default=str).encode()).hexdigest())
    return result


def http(path, expected, method='GET', body=None):
    request = Request(base + path, method=method,
                      headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                      data=json.dumps(body).encode() if body is not None else None)
    try:
        with urlopen(request, timeout=10) as response:
            code, data = response.status, json.load(response)
    except HTTPError as error:
        code, data = error.code, json.load(error)
    assert code == expected, (method, path, code, data)
    print(method, path, code)
    return data


before = snapshot()
expected = list(ClienteSerializer(Cliente.objects.all(), many=True).data)
assert http('/clientes', 200) == expected
cliente = Cliente.objects.get(pk=1)
assert http('/clientes/1', 200) == ClienteSerializer(cliente).data
assert not Cliente.objects.filter(pk=999999999).exists(), 'ID de prueba ya existe'
assert http('/clientes/999999999', 404) == {'detail': 'Cliente no encontrado.'}
for path in ['/', '/api/', '/api/categorias/', '/api/clientes/', '/api/productos/', '/api/pedidos/', '/api/items/']:
    data = http(path, 200)
    if path == '/api/clientes/':
        assert data['count'] == len(expected)
        assert data['results'] == expected[:100]
http('/api/clientes/', 200, method='OPTIONS')
http('/api/clientes/', 400, method='POST', body={'nombre': '', 'email': 'correo-invalido'})
# CREATE real DRF, validacion real y llamada ORM comprobada; solo create() se simula.
# No hay INSERT ni consumo de ID en MariaDB.
body = {'nombre': 'Validacion READ sin insertar', 'email': uuid.uuid4().hex + '@example.test'}
request = APIRequestFactory().post('/api/clientes/', body, format='json')
with patch.object(Cliente.objects, 'create', return_value=Cliente(pk=0, **body)) as crear:
    response = ClienteView.as_view()(request)
    assert response.status_code == 201, response.data
    assert response.data['nombre'] == body['nombre']
    crear.assert_called_once_with(**body)
print('CREATE 201 con validacion real y persistencia ORM simulada; sin INSERT.')
assert snapshot() == before, 'Se detecto un cambio de datos durante la verificacion'
print('READ_OK: respuestas coinciden con MariaDB. Tablas de negocio sin cambios:',
      {table: count for table, (count, digest) in before.items()})

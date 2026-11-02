"""Sesion controlada: solo clientes temporales creados despues de la instantanea.
Ejecutar por etapas desde Cmder; no se toca el cliente 1 ni se crean pedidos.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u2_proyecto1.settings')
import django
django.setup()
from django.db import connection
from pedidos_app.models import Cliente, Pedido
from pedidos_app.serializers import ClienteSerializer

path = root / '.local/update_delete_sesion.json'
base = 'http://127.0.0.1:8000'
emails = {'patch': 'crud-temp-patch-021126@example.test',
          'delete': 'crud-temp-delete-021126@example.test'}
updated_email = 'crud-temp-patch-actualizado-021126@example.test'


def snapshot(excluir=()):
    result = {}
    with connection.cursor() as cursor:
        for table in sorted(connection.introspection.table_names()):
            if not table.startswith(('pedidos_app_', 'productos_app_')):
                continue
            cursor.execute('SELECT * FROM ' + connection.ops.quote_name(table) + ' ORDER BY id')
            rows = cursor.fetchall()
            if table == 'pedidos_app_cliente':
                rows = [row for row in rows if row[0] not in excluir]
            result[table] = {'count': len(rows), 'sha256': hashlib.sha256(json.dumps(rows, default=str).encode()).hexdigest()}
    return result


def http(method, endpoint, expected, body=None):
    request = Request(base + endpoint, method=method,
                      headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                      data=json.dumps(body).encode() if body is not None else None)
    try:
        with urlopen(request, timeout=10) as response:
            code, raw = response.status, response.read()
    except HTTPError as error:
        code, raw = error.code, error.read()
    data = json.loads(raw) if raw else None
    assert code == expected, (method, endpoint, code, data)
    print(method, endpoint, code, json.dumps(data, ensure_ascii=False))
    return data


def comprobar_originales(state):
    assert ClienteSerializer(Cliente.objects.get(pk=1)).data == state['original_1']
    assert snapshot(state.get('temporales', {}).values()) == state['baseline'], 'Hay cambios fuera de los temporales: revisar'
    print('ORIGINALES_INTACTOS: cliente 1, otros clientes, pedidos, items y demas tablas coinciden.')


def temporal(state, tipo):
    pk = state['temporales'][tipo]
    assert pk != 1 and pk not in state['ids_iniciales'], 'No es un cliente de esta prueba'
    obj = Cliente.objects.get(pk=pk)
    assert not Pedido.objects.filter(cliente_id=pk).exists(), 'Temporal con pedidos: no modificar ni eliminar automaticamente'
    return obj


if len(sys.argv) != 2:
    raise SystemExit('Usar --preparar, --registrar, --nombre, --correo, --validaciones, --eliminado o --limpiar')
step = sys.argv[1]
if step == '--preparar':
    assert not path.exists(), 'Ya existe sesion: revisar antes de iniciar otra; no sobrescribir evidencia'
    assert not Cliente.objects.filter(email__in=[*emails.values(), updated_email]).exists(), 'Ya existen correos reservados; no duplicar'
    assert not Cliente.objects.filter(pk=999999999).exists(), 'ID de prueba 404 ya existe'
    state = {'ids_iniciales': list(Cliente.objects.values_list('pk', flat=True)),
             'original_1': dict(ClienteSerializer(Cliente.objects.get(pk=1)).data),
             'baseline': snapshot(), 'temporales': {}, 'etapas': []}
else:
    state = json.loads(path.read_text(encoding='utf-8'))
    assert not state.get('terminada'), 'Sesion ya terminada; no repetir mutaciones'

if step == '--registrar':
    assert not state['temporales'], 'Los temporales ya fueron registrados'
    for tipo, email in emails.items():
        obj = Cliente.objects.get(email=email)
        assert obj.pk not in state['ids_iniciales'] and obj.pk != 1
        assert not Pedido.objects.filter(cliente_id=obj.pk).exists()
        state['temporales'][tipo] = obj.pk
        print('TEMPORAL ANTES', tipo, dict(ClienteSerializer(obj).data))
elif step == '--nombre':
    obj = temporal(state, 'patch')
    assert obj.nombre == 'Temporal PATCH actualizado' and obj.email == emails['patch']
    print('PATCH_NOMBRE_OK: correo no enviado conservado.', dict(ClienteSerializer(obj).data))
elif step == '--correo':
    obj = temporal(state, 'patch')
    assert obj.nombre == 'Temporal PATCH actualizado' and obj.email == updated_email
    print('PATCH_CORREO_OK: nombre no enviado conservado.', dict(ClienteSerializer(obj).data))
elif step == '--validaciones':
    obj = temporal(state, 'patch')
    before = dict(ClienteSerializer(obj).data)
    for body in [{'id': obj.pk, 'email': 'correo-invalido'},
                 {'id': obj.pk, 'nombre': ''},
                 {'id': obj.pk, 'email': state['original_1']['email']},
                 {'id': obj.pk}, {'id': True, 'nombre': 'Error'},
                 {'id': str(obj.pk), 'nombre': 'Error'}]:
        http('PATCH', '/cliente/modificar', 400, body)
    http('PATCH', '/cliente/modificar', 404, {'id': 999999999, 'nombre': 'No existe'})
    http('DELETE', '/cliente/eliminar', 404, {'id': 999999999})
    http('DELETE', '/cliente/eliminar', 400, {})
    obj.refresh_from_db()
    assert dict(ClienteSerializer(obj).data) == before
    print('VALIDACIONES_OK: no cambiaron los datos ante los errores.')
elif step == '--eliminado':
    pk = state['temporales']['delete']
    assert pk != 1 and pk not in state['ids_iniciales']
    assert not Cliente.objects.filter(pk=pk).exists()
    http('GET', '/clientes/' + str(pk), 404)
    print('DELETE_SQL_OK: temporal DELETE ausente en MariaDB, ID', pk)
elif step == '--limpiar':
    assert '--eliminado' in state['etapas'], 'Confirmar antes la eliminacion visual'
    obj = temporal(state, 'patch')
    assert obj.nombre == 'Temporal PATCH actualizado' and obj.email == updated_email
    http('DELETE', '/cliente/eliminar', 204, {'id': obj.pk})
    assert not Cliente.objects.filter(pk__in=state['temporales'].values()).exists()
    assert snapshot() == state['baseline'], 'Datos finales distintos de los iniciales'
    state['terminada'] = True
    print('SESION_TERMINADA: los dos temporales fueron retirados; filas originales intactas. El contador de IDs puede avanzar.')
elif step != '--preparar':
    raise SystemExit('Etapa no reconocida')

comprobar_originales(state)
state['etapas'].append(step)
path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
print('Etapa verificada:', step)

"""Sesion visual controlada, con comprobacion de todas las filas originales."""
import json, os, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u2_proyecto1.settings')
import django
django.setup()
from django.db import connection
from pedidos_app.models import Categoria, Producto, Cliente, Pedido, Item
from pedidos_app.serializers import ProductoSerializer
path = root / '.local/catalogo_sesion.json'
base = 'http://127.0.0.1:8000'


def rows():
    result = {}
    with connection.cursor() as c:
        for table in sorted(connection.introspection.table_names()):
            if table.startswith(('pedidos_app_', 'productos_app_')):
                c.execute('SELECT * FROM ' + connection.ops.quote_name(table) + ' ORDER BY id')
                result[table] = json.loads(json.dumps(c.fetchall(), default=str))
    return result


def save():
    path.write_text(json.dumps(s, indent=2), encoding='utf-8')


def http(method, url, code, body=None):
    req = Request(base+url, method=method, data=json.dumps(body).encode() if body is not None else None,
                  headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urlopen(req, timeout=15) as r:
            actual, raw = r.status, r.read()
    except HTTPError as e:
        actual, raw = e.code, e.read()
    data = json.loads(raw) if raw else None
    assert actual == code, (method, url, actual, data)
    print(method, url, actual, json.dumps(data, ensure_ascii=False))
    return data


def own(table, pk):
    assert pk not in [r[0] for r in s['antes'][table]], 'ID preexistente: no tocar'
    s['propios'].setdefault(table, [])
    if pk not in s['propios'][table]:
        s['propios'][table].append(pk)
    save()
    return pk


def check():
    actual = rows()
    for table, original in s['antes'].items():
        nuevos = s['propios'].get(table, [])
        assert [r for r in actual[table] if r[0] not in nuevos] == original, 'Cambios ajenos: '+table
    print('ORIGINALES_INTACTOS: todas las filas de negocio, M2M, clientes, pedidos e items.')


step = sys.argv[1]
if step == '--preparar':
    assert not path.exists(), 'Sesion existente: revisar antes de repetir'
    assert not Categoria.objects.filter(nombre__startswith='TEMP Catalogo 021126').exists()
    assert not Producto.objects.filter(codigo='TEMP-CAT-021126').exists()
    s = {'antes': rows(), 'propios': {}, 'ids': {}, 'etapas': []}
else:
    s = json.loads(path.read_text(encoding='utf-8'))
    assert not s.get('terminada'), 'Sesion ya terminada'
ids = s['ids']
if step == '--categoria':
    obj = Categoria.objects.get(nombre='TEMP Catalogo 021126 A')
    ids['categoria'] = own('pedidos_app_categoria', obj.pk)
    print('CATEGORIA_SQL', obj.pk, obj.nombre)
elif step == '--categoria-modificada':
    obj = Categoria.objects.get(pk=ids['categoria'])
    assert obj.nombre == 'TEMP Catalogo 021126 A editada'
    print('CATEGORIA_MODIFICADA_SQL', obj.pk, obj.nombre)
    obj = http('POST', '/categoria/agregar', 201, {'nombre': 'TEMP Catalogo 021126 B'})
    ids['segunda'] = own('pedidos_app_categoria', obj['id'])
elif step == '--producto':
    obj = Producto.objects.get(codigo='TEMP-CAT-021126')
    ids['producto'] = own('pedidos_app_producto', obj.pk)
    for pk in Producto.categorias.through.objects.filter(producto_id=obj.pk).values_list('pk', flat=True):
        own('pedidos_app_producto_categorias', pk)
    assert list(obj.categorias.values_list('pk', flat=True)) == [ids['categoria']]
    s['creado'] = str(obj.creado)
    print('PRODUCTO_ANTES_SQL', dict(ProductoSerializer(obj).data))
elif step == '--producto-modificado':
    obj = Producto.objects.get(pk=ids['producto'])
    for pk in Producto.categorias.through.objects.filter(producto_id=obj.pk).values_list('pk', flat=True):
        own('pedidos_app_producto_categorias', pk)
    assert obj.nombre == 'TEMP Producto editado' and obj.precio == 3200 and obj.stock == 7
    assert list(obj.categorias.values_list('pk', flat=True)) == [ids['segunda']]
    assert str(obj.creado) == s['creado']
    print('PRODUCTO_DESPUES_SQL', dict(ProductoSerializer(obj).data))
elif step == '--validar':
    http('POST', '/categoria/agregar', 400, {'nombre': 'TEMP Catalogo 021126 A editada'})
    http('PATCH', '/categoria/modificar', 400, {'id': ids['categoria'], 'nombre': 'TEMP Catalogo 021126 B'})
    for body in [{'id': ids['producto'], 'precio': -1}, {'id': ids['producto'], 'stock': -1},
                 {'id': ids['producto'], 'categorias': [999999999]},
                 {'id': ids['producto'], 'creado': '2020-01-01'}]:
        http('PATCH', '/producto/modificar', 400, body)
    for entidad in ['categoria', 'producto']:
        http('PATCH', '/'+entidad+'/modificar', 404, {'id': 999999999, 'nombre': 'Ausente'})
        http('DELETE', '/'+entidad+'/eliminar', 404, {'id': 999999999})
    # Omision de categorias conserva las asociaciones.
    before = list(Producto.objects.get(pk=ids['producto']).categorias.values_list('pk', flat=True))
    http('PATCH', '/producto/modificar', 200, {'id': ids['producto'], 'descripcion': 'Solo descripcion'})
    assert list(Producto.objects.get(pk=ids['producto']).categorias.values_list('pk', flat=True)) == before
elif step == '--proteger':
    obj = http('POST', '/api/clientes/', 201, {'nombre': 'TEMP Catalogo', 'email': 'temp-catalogo-021126@example.test'})
    ids['cliente'] = own('pedidos_app_cliente', obj['id'])
    http('PATCH', '/cliente/modificar', 200, {'id': ids['cliente'], 'nombre': 'TEMP Catalogo editado'})
    http('GET', '/clientes/'+str(ids['cliente']), 200)
    http('GET', '/clientes', 200)
    obj = http('POST', '/api/pedidos/', 201, {'cliente': ids['cliente'], 'fecha': '2026-11-02', 'pagado': False})
    ids['pedido'] = own('pedidos_app_pedido', obj['id'])
    obj = http('POST', '/api/items/', 201, {'pedido': ids['pedido'], 'producto': ids['producto'], 'cantidad': 1, 'precio_unitario': 3200})
    ids['item'] = own('pedidos_app_item', obj['id'])
    print('PROTECCION_PREPARADA', ids)
elif step == '--liberar':
    # Retirar exclusivamente el Item creado por esta sesion; nunca borrar para eludir datos originales.
    assert ids['item'] in s['propios']['pedidos_app_item']
    item = Item.objects.get(pk=ids['item'])
    assert item.pedido_id == ids['pedido'] and item.producto_id == ids['producto']
    http('DELETE', '/producto/eliminar', 409, {'id': ids['producto']})
    http('DELETE', '/categoria/eliminar', 409, {'id': ids['segunda']})
    item.delete()
    pedido = Pedido.objects.get(pk=ids['pedido'])
    assert pedido.cliente_id == ids['cliente'] and not Item.objects.filter(pedido=pedido).exists()
    pedido.delete()
    http('DELETE', '/cliente/eliminar', 204, {'id': ids['cliente']})
    print('RELACIONES_TEMPORALES_RETIRADAS; producto y categorias listos para DELETE visual.')
elif step == '--final':
    assert not Producto.objects.filter(pk=ids['producto']).exists()
    assert not Categoria.objects.filter(pk=ids['categoria']).exists()
    http('GET', '/productos/'+str(ids['producto']), 404)
    http('GET', '/categorias/'+str(ids['categoria']), 404)
    assert not Producto.objects.filter(categorias=ids['segunda']).exists()
    http('DELETE', '/categoria/eliminar', 204, {'id': ids['segunda']})
    assert rows() == s['antes'], 'Datos finales diferentes'
    s['terminada'] = True
    print('CATALOGO_TERMINADO: temporales retirados, filas originales intactas; contadores pueden avanzar.')
elif step != '--preparar':
    raise SystemExit('Etapa no reconocida')
check()
s['etapas'].append(step)
save()

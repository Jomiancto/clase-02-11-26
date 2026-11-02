"""Inspeccion de lectura antes o despues de migrar; no muestra credenciales."""
import json
import os
from pathlib import Path
import sys

raiz = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(raiz))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u2_proyecto1.settings')
import django
django.setup()
from django.conf import settings
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

with connection.cursor() as cursor:
    cursor.execute('SELECT VERSION(), DATABASE(), @@port, @@datadir')
    print('Servidor, base, puerto, directorio:', cursor.fetchone())
    print('Tablas existentes:', sorted(connection.introspection.table_names(cursor)))
    cursor.execute('SELECT app, name FROM django_migrations ORDER BY app, name')
    print('Migraciones aplicadas:', cursor.fetchall())
ejecutor = MigrationExecutor(connection)
plan = ejecutor.migration_plan(ejecutor.loader.graph.leaf_nodes())
print('Plan:', [(m.app_label, m.name, atras) for m, atras in plan])
if '--antes' in sys.argv:
    previstas = {'0001_initial', '0002_pedido', '0003_producto_categorias_item'}
    if any(m.app_label != 'pedidos_app' or m.name not in previstas or atras for m, atras in plan):
        raise SystemExit('Plan distinto del avance revisado del profesor; no aplicar automaticamente.')
    if plan and any(t.startswith('pedidos_app_') for t in connection.introspection.table_names()):
        raise SystemExit('Ya existen tablas pedidos_app con migraciones pendientes; revisar conflicto.')
    print('PREVIA_OK: operaciones previstas de pedidos_app; no se modificaron datos.')
if '--despues' in sys.argv:
    from pedidos_app.models import Categoria, Cliente, Producto, Pedido, Item
    from django.db.models import CASCADE, PROTECT
    modelos = [Categoria, Cliente, Producto, Pedido, Item, Producto.categorias.through]
    todas = set(connection.introspection.table_names())
    resumen = {}
    with connection.cursor() as cursor:
        for modelo in modelos:
            tabla = modelo._meta.db_table
            assert tabla in todas, tabla
            restricciones = connection.introspection.get_constraints(cursor, tabla)
            assert any(r['primary_key'] for r in restricciones.values()), tabla
            for campo in modelo._meta.fields:
                if campo.many_to_one:
                    destino = (campo.remote_field.model._meta.db_table, campo.target_field.column)
                    assert any(r.get('foreign_key') == destino and campo.column in r['columns'] for r in restricciones.values()), (tabla, campo.name)
            resumen[tabla] = {nombre: {'columnas': r['columns'], 'pk': r['primary_key'],
                                      'unico': r['unique'], 'fk': r.get('foreign_key')}
                              for nombre, r in restricciones.items()}
        for modelo, columna in [(Cliente, 'email'), (Categoria, 'nombre')]:
            restricciones = connection.introspection.get_constraints(cursor, modelo._meta.db_table)
            assert any(r['unique'] and r['columns'] == [columna] for r in restricciones.values())
    assert Pedido._meta.get_field('cliente').remote_field.on_delete is CASCADE
    assert Item._meta.get_field('pedido').remote_field.on_delete is CASCADE
    assert Item._meta.get_field('producto').remote_field.on_delete is PROTECT
    with connection.cursor() as cursor:
        intermedia = connection.introspection.get_constraints(cursor, Producto.categorias.through._meta.db_table)
        assert any(r['unique'] and set(r['columns']) == {'producto_id', 'categoria_id'} for r in intermedia.values())
    assert not plan, 'Quedan migraciones pendientes'
    print(json.dumps(resumen, ensure_ascii=False, indent=2, default=str))
    print('Conteos:', {m.__name__: m.objects.count() for m in modelos})
    print('RELACIONES_OK: seis tablas, PK, FK, campos unicos y politicas ORM verificadas.')

"""Pruebas de contrato y persistencia sobre base de pruebas aislada."""
from unittest.mock import patch
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Categoria, Producto, Cliente, Pedido, Item
from .serializers import ProductoSerializer


class CatalogoTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.a = Categoria.objects.create(nombre='A')
        self.b = Categoria.objects.create(nombre='B')
        self.p = Producto.objects.create(nombre='Inicial', descripcion='Texto', precio=100, stock=2, codigo='TEST')
        self.p.categorias.set([self.a])

    def producto(self, **extra):
        return dict(nombre='Nuevo', descripcion='Ejemplo', precio=2500, stock=4,
                    activo=True, codigo='NUEVO', categorias=[self.a.pk], **extra)

    def test_categoria_create_persistencia_y_duplicado(self):
        r = self.api.post('/categoria/agregar', {'nombre': 'Nueva'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Categoria.objects.get(pk=r.data['id']).nombre, 'Nueva')
        self.assertEqual(self.api.post('/categoria/agregar', {'nombre': 'Nueva'}, format='json').status_code, 400)

    def test_categoria_campos_invalidos(self):
        for body in [{}, {'nombre': ''}, {'nombre': 'x'*81}, {'nombre': 'C', 'id': 20}, []]:
            with self.subTest(body=body):
                self.assertEqual(self.api.post('/categoria/agregar', body, format='json').status_code, 400)
        self.assertEqual(Categoria.objects.count(), 2)

    def test_categoria_read(self):
        r = self.api.get('/categorias')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)
        self.assertEqual(self.api.get(f'/categorias/{self.a.pk}').data['nombre'], 'A')
        self.assertEqual(self.api.get('/categorias/999999999').status_code, 404)

    def test_listados_vacios(self):
        self.p.delete()
        Categoria.objects.all().delete()
        for url in ['/categorias', '/productos']:
            r = self.api.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.data, [])

    def test_categoria_patch(self):
        r = self.api.patch('/categoria/modificar', {'id': self.b.pk, 'nombre': 'Renombrada'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.b.refresh_from_db()
        self.assertEqual(self.b.nombre, 'Renombrada')
        self.assertEqual(self.api.patch('/categoria/modificar', {'id': self.b.pk, 'nombre': 'A'}, format='json').status_code, 400)
        self.b.refresh_from_db()
        self.assertEqual(self.b.nombre, 'Renombrada')

    def test_categoria_delete_libre(self):
        r = self.api.delete('/categoria/eliminar', {'id': self.b.pk}, format='json')
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.content, b'')
        self.assertFalse(Categoria.objects.filter(pk=self.b.pk).exists())

    def test_categoria_delete_asociada_409(self):
        self.assertEqual(self.api.delete('/categoria/eliminar', {'id': self.a.pk}, format='json').status_code, 409)
        self.assertTrue(Categoria.objects.filter(pk=self.a.pk).exists())
        self.assertEqual(list(self.p.categorias.values_list('pk', flat=True)), [self.a.pk])

    def test_producto_create_m2m(self):
        r = self.api.post('/producto/agregar', self.producto(), format='json')
        self.assertEqual(r.status_code, 201)
        obj = Producto.objects.get(pk=r.data['id'])
        self.assertEqual(obj.precio, 2500)
        self.assertTrue(obj.activo)
        self.assertEqual(list(obj.categorias.values_list('pk', flat=True)), [self.a.pk])
        self.assertTrue(r.data['creado'])

    def test_producto_invalidos_sin_insert(self):
        casos = [{}, {'stock': -1}, {'precio': -1}, {'categorias': [999999999]},
                 {'categorias': []}, {'nombre': ''}, {'codigo': 'x'*21}, {'stock': 'error'},
                 {'activo': 'no-es-booleano'}, {'creado': '2020-01-01'}, {'id': 1}, {'otro': 1}]
        for datos in casos:
            body = self.producto()
            if not datos:
                body = {}
            else:
                body.update(datos)
            with self.subTest(body=body):
                self.assertEqual(self.api.post('/producto/agregar', body, format='json').status_code, 400)
        self.assertEqual(Producto.objects.count(), 1)

    def test_producto_cero_conforme_modelo(self):
        body = self.producto()
        body.update(precio=0, stock=0)
        self.assertEqual(self.api.post('/producto/agregar', body, format='json').status_code, 201)

    def test_producto_read(self):
        r = self.api.get('/productos')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['categorias'], [self.a.pk])
        r = self.api.get(f'/productos/{self.p.pk}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['codigo'], 'TEST')
        self.assertEqual(self.api.get('/productos/999999999').status_code, 404)

    def test_producto_patch_omite_categorias(self):
        creado = self.p.creado
        r = self.api.patch('/producto/modificar', {'id': self.p.pk, 'nombre': 'Parcial'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.p.refresh_from_db()
        self.assertEqual(self.p.nombre, 'Parcial')
        self.assertEqual(self.p.precio, 100)
        self.assertEqual(self.p.creado, creado)
        self.assertEqual(list(self.p.categorias.values_list('pk', flat=True)), [self.a.pk])

    def test_producto_patch_campos_y_categorias(self):
        body = dict(id=self.p.pk, nombre='Editado', descripcion='Cambio', precio=900,
                    stock=10, activo=True, codigo='EDITADO', categorias=[self.b.pk])
        r = self.api.patch('/producto/modificar', body, format='json')
        self.assertEqual(r.status_code, 200)
        self.p.refresh_from_db()
        self.assertEqual((self.p.nombre, self.p.descripcion, self.p.precio, self.p.stock,
                          self.p.activo, self.p.codigo), ('Editado', 'Cambio', 900, 10, True, 'EDITADO'))
        self.assertEqual(list(self.p.categorias.values_list('pk', flat=True)), [self.b.pk])

    def test_producto_patch_invalido_atomico(self):
        for datos in [{'categorias': [999999999]}, {'precio': -1}, {'stock': -1},
                      {'creado': '2020-01-01'}, {'codigo': 'x'*21}]:
            body = {'id': self.p.pk, 'nombre': 'No guardar', **datos}
            self.assertEqual(self.api.patch('/producto/modificar', body, format='json').status_code, 400)
        self.p.refresh_from_db()
        self.assertEqual(self.p.nombre, 'Inicial')
        self.assertEqual(list(self.p.categorias.values_list('pk', flat=True)), [self.a.pk])

    def test_rollback_producto_y_m2m_ante_error_guardado(self):
        def fallo(serializer):
            obj = Producto.objects.create(nombre='No persistir', precio=0, stock=0, codigo='FALLO')
            obj.categorias.add(self.b)
            raise IntegrityError('fallo controlado despues del INSERT y M2M')
        with patch.object(ProductoSerializer, 'save', fallo):
            r = self.api.post('/producto/agregar', self.producto(), format='json')
        self.assertEqual(r.status_code, 400)
        self.assertFalse(Producto.objects.filter(codigo='FALLO').exists())
        self.assertEqual(Producto.categorias.through.objects.count(), 1)

    def test_producto_delete_libre(self):
        r = self.api.delete('/producto/eliminar', {'id': self.p.pk}, format='json')
        self.assertEqual(r.status_code, 204)
        self.assertFalse(Producto.objects.filter(pk=self.p.pk).exists())
        self.assertEqual(Producto.categorias.through.objects.count(), 0)
        self.assertTrue(Categoria.objects.filter(pk=self.a.pk).exists())

    def test_producto_protect_item_409(self):
        c = Cliente.objects.create(nombre='Temporal', email='protect@example.test')
        pedido = Pedido.objects.create(cliente=c, fecha='2026-11-02', pagado=False)
        item = Item.objects.create(pedido=pedido, producto=self.p, cantidad=1, precio_unitario=100)
        self.assertEqual(self.api.delete('/producto/eliminar', {'id': self.p.pk}, format='json').status_code, 409)
        self.assertTrue(Producto.objects.filter(pk=self.p.pk).exists())
        self.assertTrue(Item.objects.filter(pk=item.pk).exists())
        self.assertTrue(Pedido.objects.filter(pk=pedido.pk).exists())

    def test_identificacion_y_errores(self):
        for entidad in ['categoria', 'producto']:
            for method, action in [('patch', 'modificar'), ('delete', 'eliminar')]:
                call = getattr(self.api, method)
                for body in [{}, {'id': True}, {'id': '1'}, {'id': 0}, {'id': 1.5}, []]:
                    self.assertEqual(call(f'/{entidad}/{action}', body, format='json').status_code, 400)
                body = {'id': 999999999}
                if method == 'patch':
                    body['nombre'] = 'Inexistente'
                self.assertEqual(call(f'/{entidad}/{action}', body, format='json').status_code, 404)
                self.assertEqual(call(f'/{entidad}/{action}', {'id': self.a.pk, 'extra': 1}, format='json').status_code, 400)
            self.assertEqual(self.api.patch(f'/{entidad}/modificar', {'id': 1}, format='json').status_code, 400)

    def test_metodos_restringidos(self):
        for entidad in ['categoria', 'producto']:
            for action in ['agregar', 'modificar', 'eliminar']:
                self.assertEqual(self.api.get(f'/{entidad}/{action}').status_code, 405)

    def test_api_anterior_conservada(self):
        for entidad in ['categorias', 'productos', 'clientes', 'pedidos', 'items']:
            self.assertEqual(self.api.get(f'/api/{entidad}/').status_code, 200)
        self.assertEqual(self.api.post('/api/categorias/', {'nombre': 'API anterior'}, format='json').status_code, 201)
        self.assertEqual(self.api.post('/api/productos/', self.producto(), format='json').status_code, 201)

    def test_regresion_cliente_crud_persistencia(self):
        r = self.api.post('/api/clientes/', {'nombre': 'Prueba', 'email': 'crud@example.test'}, format='json')
        self.assertEqual(r.status_code, 201)
        pk = r.data['id']
        self.assertEqual(self.api.get('/clientes').status_code, 200)
        self.assertEqual(self.api.get(f'/clientes/{pk}').status_code, 200)
        self.assertEqual(self.api.patch('/cliente/modificar', {'id': pk, 'nombre': 'Modificado'}, format='json').status_code, 200)
        self.assertEqual(Cliente.objects.get(pk=pk).nombre, 'Modificado')
        self.assertEqual(self.api.delete('/cliente/eliminar', {'id': pk}, format='json').status_code, 204)
        self.assertFalse(Cliente.objects.filter(pk=pk).exists())
        self.assertEqual(self.api.get(f'/clientes/{pk}').status_code, 404)

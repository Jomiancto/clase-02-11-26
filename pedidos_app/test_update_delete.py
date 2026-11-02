"""Validacion y proteccion de CASCADE sin tocar registros reales."""
from contextlib import nullcontext
from unittest.mock import Mock, patch
from django.test import SimpleTestCase
from rest_framework.test import APIClient
from .models import Cliente


class ClienteUpdateDeleteTests(SimpleTestCase):
    def setUp(self):
        self.api = APIClient()
        self.cliente = Cliente(id=42, nombre='Temporal', email='temporal@example.test')
        self.atomic = patch('pedidos_app.views.transaction.atomic', side_effect=lambda: nullcontext())
        self.atomic.start()
        self.addCleanup(self.atomic.stop)
        self.consulta = patch('pedidos_app.views.Cliente.objects.select_for_update')
        self.seleccionar = self.consulta.start()
        self.addCleanup(self.consulta.stop)
        self.seleccionar.return_value.get.return_value = self.cliente

    def test_ids_invalidos_no_consultan_orm(self):
        for metodo, ruta in [('patch', '/cliente/modificar'), ('delete', '/cliente/eliminar')]:
            for identificador in [None, True, False, 0, -1, '42', 1.5, [], 9223372036854775808]:
                with self.subTest(metodo=metodo, identificador=identificador):
                    response = getattr(self.api, metodo)(ruta, {'id': identificador, **({'nombre': 'Cambio'} if metodo == 'patch' else {})}, format='json')
                    self.assertEqual(response.status_code, 400)
        self.seleccionar.assert_not_called()

    def test_json_debe_ser_objeto(self):
        for metodo, ruta in [('patch', '/cliente/modificar'), ('delete', '/cliente/eliminar')]:
            response = getattr(self.api, metodo)(ruta, [42], format='json')
            self.assertEqual(response.status_code, 400)
        self.seleccionar.assert_not_called()

    def test_cliente_inexistente(self):
        self.seleccionar.return_value.get.side_effect = Cliente.DoesNotExist
        for metodo, ruta, body in [('patch', '/cliente/modificar', {'id': 999999999, 'nombre': 'Cambio'}),
                                   ('delete', '/cliente/eliminar', {'id': 999999999})]:
            response = getattr(self.api, metodo)(ruta, body, format='json')
            self.assertEqual(response.status_code, 404)

    def test_patch_parcial_conserva_email(self):
        with patch.object(self.cliente, 'save') as guardar:
            response = self.api.patch('/cliente/modificar', {'id': 42, 'nombre': 'Modificado'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nombre'], 'Modificado')
        self.assertEqual(response.data['email'], 'temporal@example.test')
        self.seleccionar.return_value.get.assert_called_once_with(pk=42)
        guardar.assert_called_once()

    def test_patch_rechaza_nombre_vacio(self):
        with patch.object(self.cliente, 'save') as guardar:
            response = self.api.patch('/cliente/modificar', {'id': 42, 'nombre': ''}, format='json')
        self.assertEqual(response.status_code, 400)
        guardar.assert_not_called()

    def test_patch_sin_cambios_o_campos_desconocidos(self):
        for body in [{'id': 42}, {'id': 42, 'nombre': 'Otro', 'otro_id': 1}]:
            self.assertEqual(self.api.patch('/cliente/modificar', body, format='json').status_code, 400)
        self.seleccionar.assert_not_called()

    def test_delete_con_pedidos_no_llama_delete(self):
        with patch('pedidos_app.views.Pedido.objects.filter') as pedidos, patch.object(self.cliente, 'delete') as borrar:
            pedidos.return_value.exists.return_value = True
            response = self.api.delete('/cliente/eliminar', {'id': 42}, format='json')
        self.assertEqual(response.status_code, 409)
        pedidos.assert_called_once_with(cliente_id=42)
        borrar.assert_not_called()

    def test_delete_sin_pedidos_devuelve_204(self):
        with patch('pedidos_app.views.Pedido.objects.filter') as pedidos, patch.object(self.cliente, 'delete') as borrar:
            pedidos.return_value.exists.return_value = False
            response = self.api.delete('/cliente/eliminar', {'id': 42}, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        borrar.assert_called_once_with()

    def test_delete_rechaza_campos_extra(self):
        response = self.api.delete('/cliente/eliminar', {'id': 42, 'nombre': 'Otro'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.seleccionar.assert_not_called()

    def test_metodos_no_habilitados(self):
        self.assertEqual(self.api.get('/cliente/modificar').status_code, 405)
        self.assertEqual(self.api.post('/cliente/eliminar', {'id': 42}, format='json').status_code, 405)

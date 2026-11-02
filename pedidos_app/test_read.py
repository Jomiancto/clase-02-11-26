"""READ sin escrituras en base de datos: consultas ORM simuladas."""
from unittest.mock import patch
from django.test import SimpleTestCase
from rest_framework.test import APIClient
from .models import Cliente


class ClienteReadTests(SimpleTestCase):
    def setUp(self):
        self.api = APIClient()
        self.cliente = Cliente(id=1, nombre='Cliente de clase', email='clase@example.test')

    @patch('pedidos_app.views.Cliente.objects.all')
    def test_listar_clientes(self, consultar):
        consultar.return_value = [self.cliente]
        response = self.api.get('/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': 1, 'nombre': 'Cliente de clase', 'email': 'clase@example.test'}])
        consultar.assert_called_once_with()

    @patch('pedidos_app.views.Cliente.objects.all', return_value=[])
    def test_lista_vacia(self, consultar):
        response = self.api.get('/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('pedidos_app.views.Cliente.objects.get')
    def test_cliente_existente(self, consultar):
        consultar.return_value = self.cliente
        response = self.api.get('/clientes/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], 'clase@example.test')
        consultar.assert_called_once_with(pk=1)

    @patch('pedidos_app.views.Cliente.objects.get', side_effect=Cliente.DoesNotExist)
    def test_cliente_inexistente(self, consultar):
        response = self.api.get('/clientes/999999999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Cliente no encontrado.'})

    def test_read_no_admite_post(self):
        for path in ['/clientes', '/clientes/1']:
            response = self.api.post(path, {}, format='json')
            self.assertEqual(response.status_code, 405)

from django.db import transaction
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Categoria, Producto, Cliente, Pedido, Item
from .serializers import (CategoriaSerializer, ProductoSerializer, ClienteSerializer,
                          PedidoSerializer, ItemSerializer)


@api_view(['GET'])
def inicio(request):
    return Response({'proyecto': 'Backend Unidad 2 - CRUD', 'operaciones': ['GET', 'POST'],
                     'api': {nombre: request.build_absolute_uri('/api/' + nombre + '/')
                             for nombre in ['categorias', 'clientes', 'productos', 'pedidos', 'items']}})


class CrearListar(ListCreateAPIView):
    # Una sola transaccion incluye la relacion M2M de Producto.
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CategoriaView(CrearListar):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ClienteView(CrearListar):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProductoView(CrearListar):
    queryset = Producto.objects.prefetch_related('categorias').all()
    serializer_class = ProductoSerializer


class PedidoView(CrearListar):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class ItemView(CrearListar):
    queryset = Item.objects.order_by('id')
    serializer_class = ItemSerializer

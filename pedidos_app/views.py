from django.db import transaction
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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


@api_view(['GET'])
def listar_clientes(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClienteSerializer(cliente)
    return Response(serializer.data, status=status.HTTP_200_OK)

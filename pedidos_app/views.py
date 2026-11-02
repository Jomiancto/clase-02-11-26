from django.db import IntegrityError, transaction
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
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



def _id_cliente_json(datos):
    # Un ID JSON entero evita conversiones ambiguas o seleccionar otra fila.
    if not isinstance(datos, dict):
        raise ValidationError({'detail': 'Se requiere un objeto JSON con id.'})
    identificador = datos.get('id')
    if type(identificador) is not int or not 1 <= identificador <= 9223372036854775807:
        raise ValidationError({'id': 'Debe ser un entero positivo enviado en el JSON.'})
    return identificador


@api_view(['PATCH'])
def modificar_cliente(request):
    identificador = _id_cliente_json(request.data)
    if set(request.data) - {'id', 'nombre', 'email'}:
        raise ValidationError({'detail': 'Solo se admiten id, nombre y email.'})
    cambios = {campo: valor for campo, valor in request.data.items() if campo != 'id'}
    if not cambios:
        raise ValidationError({'detail': 'Envia nombre o email para modificar.'})
    with transaction.atomic():
        try:
            cliente = Cliente.objects.select_for_update().get(pk=identificador)
        except Cliente.DoesNotExist:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(cliente, data=cambios, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            # El savepoint permite devolver 400 sin dejar la transaccion rota.
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            return Response({'detail': 'Conflicto con un dato unico; revisa el correo.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def borrar_cliente(request):
    identificador = _id_cliente_json(request.data)
    if set(request.data) != {'id'}:
        raise ValidationError({'detail': 'DELETE solo admite el campo id.'})
    with transaction.atomic():
        try:
            # Bloquear el padre impide que se agregue un pedido entre la revision y delete.
            cliente = Cliente.objects.select_for_update().get(pk=identificador)
        except Cliente.DoesNotExist:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if Pedido.objects.filter(cliente_id=identificador).exists():
            return Response({'detail': 'No se elimina: el cliente tiene pedidos asociados. Se conservan pedidos e items.'},
                            status=status.HTTP_409_CONFLICT)
        cliente.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

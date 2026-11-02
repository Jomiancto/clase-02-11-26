from rest_framework import serializers
from .models import Categoria, Producto, Cliente, Pedido, Item


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']
        read_only_fields = ['id']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'activo', 'creado', 'codigo', 'categorias']
        read_only_fields = ['id', 'creado']


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email']
        read_only_fields = ['id']


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'fecha', 'pagado', 'cliente']
        read_only_fields = ['id']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'cantidad', 'precio_unitario', 'pedido', 'producto']
        read_only_fields = ['id']

from django.contrib import admin
from django.urls import include, path
from pedidos_app.views import inicio, listar_clientes, listar_cliente, modificar_cliente, borrar_cliente

from pedidos_app.views import (crear_categoria, listar_categorias, listar_categoria,
    modificar_categoria, borrar_categoria, crear_producto, listar_productos,
    listar_producto, modificar_producto, borrar_producto)

urlpatterns = [
    path('categoria/agregar', crear_categoria, name='crear_categoria'),
    path('categorias', listar_categorias, name='listar_categorias'),
    path('categorias/<int:id>', listar_categoria, name='listar_categoria'),
    path('categoria/modificar', modificar_categoria, name='modificar_categoria'),
    path('categoria/eliminar', borrar_categoria, name='borrar_categoria'),
    path('producto/agregar', crear_producto, name='crear_producto'),
    path('productos', listar_productos, name='listar_productos'),
    path('productos/<int:id>', listar_producto, name='listar_producto'),
    path('producto/modificar', modificar_producto, name='modificar_producto'),
    path('producto/eliminar', borrar_producto, name='borrar_producto'),
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('api/', include('pedidos_app.urls')),
    path('clientes', listar_clientes, name='listar_clientes'),
    path('clientes/<int:id>', listar_cliente, name='listar_cliente'),
    path('cliente/modificar', modificar_cliente, name='modificar_cliente'),
    path('cliente/eliminar', borrar_cliente, name='borrar_cliente'),
]

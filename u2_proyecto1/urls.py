from django.contrib import admin
from django.urls import include, path
from pedidos_app.views import inicio, listar_clientes, listar_cliente

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('api/', include('pedidos_app.urls')),
    path('clientes', listar_clientes, name='listar_clientes'),
    path('clientes/<int:id>', listar_cliente, name='listar_cliente'),
]

from django.urls import path
from . import views

app_name = 'pedidos_app'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias/', views.CategoriaView.as_view(), name='categorias'),
    path('clientes/', views.ClienteView.as_view(), name='clientes'),
    path('productos/', views.ProductoView.as_view(), name='productos'),
    path('pedidos/', views.PedidoView.as_view(), name='pedidos'),
    path('items/', views.ItemView.as_view(), name='items'),
]

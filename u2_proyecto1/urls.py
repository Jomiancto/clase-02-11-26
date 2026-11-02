from django.contrib import admin
from django.urls import include, path
from pedidos_app.views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('api/', include('pedidos_app.urls')),
]

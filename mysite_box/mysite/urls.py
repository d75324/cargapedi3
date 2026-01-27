from django.contrib import admin
from django.urls import path, include
from pedidos.admin import admin_site  # importo mi instancia para presonalizar el /admin

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('pedidos.urls')),
]

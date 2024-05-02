from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('customers/', views.customers, name='customers'),
]
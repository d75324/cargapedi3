from django.urls import path
from . import views
from . import forms

urlpatterns = [
    path('', views.home, name='home'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('customers/', views.customers, name='customers'),
    #path('add_customer/', forms.form_customers, name='add_customer'),
]
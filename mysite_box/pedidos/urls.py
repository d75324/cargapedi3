from django.urls import path
from . import views
#from . import forms

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_users, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('customers/', views.customers, name='customers'),
    path('pedidos/', views.customer_list_view, name='pedidos'),
]
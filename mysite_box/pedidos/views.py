from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def pedidos(request):
    return render(request, 'pedidos.html')

def customers(request):
    return render(request, 'customers.html')
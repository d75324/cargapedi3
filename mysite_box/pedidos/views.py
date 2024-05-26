from django.shortcuts import render, redirect
from .models import Customer
from .forms import form_customers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    # chequear que estoy logueado
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # autenticar
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Acceso Correcto")
            return redirect ('home')
        else:
            messages.success(request, "Revisar la información proporcionada")
            return redirect ('home')
    else:
        return render(request, 'home.html', {})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "Hasta pronto!")
    return redirect ('home')


def pedidos(request):
    return render(request, 'pedidos.html')

def customers(request):
    if request.method == 'POST':
        form = form_customers(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos')  # Redirige a pedidos para cargar un pedido.
    else:
        form = form_customers()
    return render(request, 'customers.html', {'form': form})

def customer_list_view(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'pedidos.html', context)

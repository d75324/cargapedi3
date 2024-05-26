from django.shortcuts import render, redirect
from .models import Customer
from .forms import form_customers

def home(request):
    return render(request, 'home.html')

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

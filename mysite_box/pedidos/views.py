from django.shortcuts import render, redirect
from .models import Customer, Order, OrderLine
from .forms import form_customers, OrderForm, OrderLineForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.forms import modelformset_factory



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


def create_order(request):
    OrderLineFormSet = modelformset_factory(OrderLine, form=OrderLineForm, extra=3, can_delete=False)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderLineFormSet(request.POST, queryset=OrderLine.objects.none())

        if order_form.is_valid() and formset.is_valid():
            # Guardamos la orden primero
            order = order_form.save()

            # Asociamos las líneas a esa orden
            for form in formset:
                if form.cleaned_data:  # Evita líneas vacías
                    order_line = form.save(commit=False)
                    order_line.order = order
                    order_line.save()

            messages.success(request, "Pedido cargado correctamente ✅")
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, "Revisá los datos del pedido, hay errores.")
    else:
        order_form = OrderForm()
        formset = OrderLineFormSet(queryset=OrderLine.objects.none())

    return render(request, 'create_order.html', {
        'order_form': order_form,
        'formset': formset,
    })

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})

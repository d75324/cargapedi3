from django import forms
from .models import Customer, Product, Order, OrderLine

class form_pedidos(forms.ModelForm):
    pass

class form_customers(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 
                  'email', 
                  'phone_number', 
                  'company_name', 
                  'company_tax_id']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'salesperson']
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'salesperson': forms.Select(attrs={'class': 'form-select'}),
        }


class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['product', 'quantity', 'vat_type']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'vat_type': forms.Select(attrs={'class': 'form-select'}),
        }

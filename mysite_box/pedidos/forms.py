from django import forms
from .models import Customer, Product

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
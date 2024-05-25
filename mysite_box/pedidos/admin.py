from django.contrib import admin
from .models import Product

class DataBackend(admin.ModelAdmin):
    list_display = (
        'sku',
        'price',
        'vat_type',
        'description',    
    )

admin.site.register(Product, DataBackend)
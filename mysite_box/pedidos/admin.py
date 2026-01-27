from django.contrib import admin
from .models import Product, Salesperson
from django.contrib.auth.models import User, Group



class DataBackEndFCO(admin.ModelAdmin):
    list_display = (
                    'sku',
                    'price',
                    'vat_type',
                    'description',
                   )
    search_fields = (
                    'sku',
                    'price',
                    'vat_type',
                    )
    list_filter = (
                    'sku',
                    'price',
                    'vat_type',
                  )    
#admin.site.register(Product, DataBackEndFCO)


class SalespersonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
      )
#admin.site.register(Salesperson, SalespersonAdmin)


# Custom admin site. Side header administration.
class MyAdminSite(admin.AdminSite):
    site_header = "Administración de Peddidos"
    #site_title = "Administración de Pedidos Site Title"
    #index_title = "Administración de Pedidos Index Title"

admin_site = MyAdminSite(name="myadmin") # instancia de la clase personalizada

admin_site.register(Product, DataBackEndFCO)
admin_site.register(Salesperson, SalespersonAdmin)
#admin_site.register(User)
#admin_site.register(Group)
admin_site.register(User)
admin_site.register(Group)

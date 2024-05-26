from django.db import models
from decimal import Decimal

# factor para calcular el valor del IVA de acuerdo al tipo
FACTOR_IVA = {
    'standard':0.21,
    'reduced':0.105,
    'zero':0,
}

class Product(models.Model):
    VAT_TYPE_CHOICES = (
    ('standard', '21%'),
    ('reduced', '10,5%'),
    ('zero', 'SIN IVA'),
    )
    sku = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_type = models.CharField(max_length=100, choices=VAT_TYPE_CHOICES, default='standard')
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.sku

class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.IntegerField(max_length=10, default=1)
    company_name = models.CharField(max_length=30)
    company_tax_id = models.IntegerField(max_length=10, default=1)

class Salesperson(models.Model):
    name = models.CharField(max_length=30, default=1)
    
    class Meta:
        app_label = 'pedidos'

# Esta clase representa una orden completa en el sistema
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=200)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)

    def calculate_subtotal(self):
        return sum(line.subtotal for line in self.orderline_set.all())
    
    def calculate_taxes(self):
        accumulated_taxes = {
            'standard': Decimal('0.00'), 
            'reduced': Decimal('0.00'), 
            'zero': Decimal('0.00')
            }
        for line in self.orderline_set.all():
            accumulated_taxes[line.vat_type] += line.calculate.iva()
        return accumulated_taxes

    def calculate_total(self):
        return self.calculate_subtotal() + sum(self.calculate_taxes().values())

# Esta clase representa una línea individual de una orden.
class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    vat_type = models.CharField(max_length=100, choices=Product.VAT_TYPE_CHOICES, default='standard')

    def calculate_subtotal(self):
        return self.product.price * self.quantity
    
    def calculate_iva(self):
        iva_para_esta_line = FACTOR_IVA[self.vat_type]
        return self.product.price * iva_para_esta_line

    def save(self, *args, **kwargs):
        self.subtotal = self.calculate_subtotal()
        super().save(*args, **kwargs)

class OrderNumber(models.Model):
    number = models.CharField(max_length=4, unique=True)

    def save(self, *args, **kwargs):
        if not self.number:
            last_order = OrderNumber.objects.last()
            if last_order:
                last_number = int(last_order.number)
                new_number = str(last_number + 1).zfill(4)  # Rellena con ceros a la izquierda
            else:
                new_number = '0000'
            self.number = new_number
        super(OrderNumber, self).save(*args, **kwargs)

    def __str__(self):
        return self.number
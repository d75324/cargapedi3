# Generated by Django 5.0.4 on 2024-12-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0008_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='vat_type',
            field=models.CharField(choices=[('standard', '21%'), ('reduced', '10,5%'), ('zero', '0%')], default='standard', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='vat_type',
            field=models.CharField(choices=[('standard', '21%'), ('reduced', '10,5%'), ('zero', '0%')], default='standard', max_length=100),
        ),
    ]
# Generated by Django 5.0.4 on 2024-05-25 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company_tax_id',
            field=models.IntegerField(default=1, max_length=10),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.IntegerField(default=1, max_length=10),
        ),
    ]

# Generated by Django 4.2.1 on 2023-08-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0002_deliveryinfo_deliveryitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryinfo',
            name='SalesOrder',
            field=models.PositiveIntegerField(),
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-04 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0026_salesemployee'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorderinfo',
            name='sales_employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sales.salesemployee'),
        ),
    ]

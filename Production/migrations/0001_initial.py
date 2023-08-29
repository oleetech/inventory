# Generated by Django 4.2.1 on 2023-08-29 08:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Sales', '0001_initial'),
        ('ItemMasterData', '0001_initial'),
        ('GeneralSettings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillOfMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('name', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ItemMasterData.item')),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('created_date', models.DateField(default=datetime.date.today)),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('docno', models.PositiveIntegerField(default=1, unique=True)),
                ('sales_order_no', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sales_production_order', to='Sales.salesorderinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('uom', models.CharField(max_length=20)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production_components', to='Production.production')),
            ],
        ),
        migrations.CreateModel(
            name='ChildComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('bill_of_materials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_components', to='Production.billofmaterials')),
                ('name', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ItemMasterData.item')),
                ('uom', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='GeneralSettings.unit')),
            ],
        ),
    ]

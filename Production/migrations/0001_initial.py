# Generated by Django 4.2.4 on 2023-08-25 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillOfMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ChildComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('uom', models.CharField(max_length=20)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('bill_of_materials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_components', to='Production.billofmaterials')),
            ],
        ),
    ]

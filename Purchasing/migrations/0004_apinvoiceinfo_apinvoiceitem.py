# Generated by Django 4.2.4 on 2023-09-01 15:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartners', '0001_initial'),
        ('Purchasing', '0003_goodsreturninfo_goodsreturnitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApInvoiceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docNo', models.PositiveIntegerField(default=1, unique=True)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('totalAmount', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('totalQty', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('customerName', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BusinessPartners.businesspartner')),
            ],
            options={
                'verbose_name': 'Ap Invoice',
                'verbose_name_plural': 'Ap Invoice',
            },
        ),
        migrations.CreateModel(
            name='ApInvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=20, null=True)),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('uom', models.CharField(default='', max_length=20, null=True)),
                ('quantity', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('price', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('priceTotal', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('order', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Purchasing.apinvoiceinfo')),
            ],
        ),
    ]
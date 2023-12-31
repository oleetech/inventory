# Generated by Django 4.2.4 on 2023-09-21 02:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BusinessPartners', '0002_alter_businesspartner_options'),
        ('Sales', '0054_alter_arinvoiceinfo_deliveryno'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docNo', models.PositiveIntegerField(default=1, unique=True)),
                ('created', models.DateField(default=datetime.date.today)),
                ('description', tinymce.models.HTMLField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('resolved', 'Resolved')], max_length=20)),
                ('customerName', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BusinessPartners.businesspartner')),
                ('deliveryNo', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='Sales.deliveryinfo')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('salesOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sales.salesorderinfo')),
            ],
            options={
                'verbose_name': 'Customer Complain ',
                'verbose_name_plural': 'Customer Complain',
            },
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-19 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0031_remove_ledgerentry_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]

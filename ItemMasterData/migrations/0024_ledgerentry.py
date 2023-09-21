# Generated by Django 4.2.4 on 2023-09-18 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0023_remove_stock_uom'),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('transaction_type', models.CharField(choices=[('STOCK', 'Stock'), ('ITEM_RECEIVED', 'Item Received'), ('ITEM_DELIVERY', 'Item Delivery'), ('ISSUE_FOR_PRODUCTION ', 'ISSUE FOR PRODUCTION')], max_length=100)),
                ('instock', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
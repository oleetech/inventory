# Generated by Django 4.2.4 on 2023-09-09 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0036_alter_productionreceiptitem_lineno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionreceiptitem',
            name='quantity',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]
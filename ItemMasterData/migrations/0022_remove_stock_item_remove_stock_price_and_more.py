# Generated by Django 4.2.4 on 2023-09-17 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0021_remove_item_warehouse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='item',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='price',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='priceTotal',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='warehouse',
        ),
    ]

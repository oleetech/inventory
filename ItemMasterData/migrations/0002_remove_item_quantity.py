# Generated by Django 4.2.4 on 2023-08-25 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0002_remove_itemreceipt_warehouse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='code',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]

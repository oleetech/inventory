# Generated by Django 4.2.3 on 2023-09-12 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0047_remove_productioncomponent_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billofmaterials",
            name="totalAmount",
        ),
        migrations.RemoveField(
            model_name="childcomponent",
            name="price",
        ),
        migrations.RemoveField(
            model_name="childcomponent",
            name="priceTotal",
        ),
    ]

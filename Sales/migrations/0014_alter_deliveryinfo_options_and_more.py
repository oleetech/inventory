# Generated by Django 4.2.3 on 2023-08-30 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0013_returninfo_returnitem"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="deliveryinfo",
            options={"verbose_name": " Delivery", "verbose_name_plural": "Delivery"},
        ),
        migrations.AlterModelOptions(
            name="salesorderinfo",
            options={
                "verbose_name": "Sales Order",
                "verbose_name_plural": "Sales Order",
            },
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-31 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0016_alter_deliveryinfo_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveryitem",
            name="orderNo",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-30 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0009_alter_productioncomponent_uom"),
    ]

    operations = [
        migrations.AlterField(
            model_name="production",
            name="sales_order_no",
            field=models.PositiveIntegerField(default=1),
        ),
    ]

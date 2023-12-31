# Generated by Django 4.2.3 on 2023-08-30 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0012_production_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="production",
            old_name="sales_order_no",
            new_name="salesOrder",
        ),
        migrations.AddField(
            model_name="productioncomponent",
            name="salesOrder",
            field=models.PositiveIntegerField(default=1),
        ),
    ]

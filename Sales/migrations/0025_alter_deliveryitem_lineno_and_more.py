# Generated by Django 4.2.3 on 2023-09-04 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0024_deliveryitem_lineno"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveryitem",
            name="lineNo",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="deliveryitem",
            name="receiptNo",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-04 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0023_remove_deliveryinfo_salesquotetion_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliveryitem",
            name="lineNo",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
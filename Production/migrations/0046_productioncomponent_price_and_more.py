# Generated by Django 4.2.3 on 2023-09-12 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0045_billofmaterials_totalamount"),
    ]

    operations = [
        migrations.AddField(
            model_name="productioncomponent",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=4, default=0, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="productioncomponent",
            name="priceTotal",
            field=models.DecimalField(
                blank=True, decimal_places=4, default=0, max_digits=10, null=True
            ),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-12 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0044_childcomponent_price_childcomponent_pricetotal"),
    ]

    operations = [
        migrations.AddField(
            model_name="billofmaterials",
            name="totalAmount",
            field=models.DecimalField(
                blank=True, decimal_places=4, default=0, max_digits=10, null=True
            ),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-05 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0031_billofmaterials_owner_production_owner_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productionreceiptitem",
            name="lineNo",
            field=models.CharField(default="1", max_length=4),
        ),
    ]

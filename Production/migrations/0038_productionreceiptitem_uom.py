# Generated by Django 4.2.3 on 2023-09-09 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0037_alter_productionreceiptitem_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="productionreceiptitem",
            name="uom",
            field=models.CharField(default="", max_length=100, null=True),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-05 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0032_alter_productionreceiptitem_lineno"),
    ]

    operations = [
        migrations.AddField(
            model_name="productionreceiptitem",
            name="orderlineNo",
            field=models.CharField(default="1", max_length=4),
        ),
    ]
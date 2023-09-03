# Generated by Django 4.2.3 on 2023-09-03 03:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Purchasing", "0004_apinvoiceinfo_apinvoiceitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="apinvoiceitem",
            name="created",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name="goodsreceiptpoitem",
            name="created",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name="goodsreturnitem",
            name="created",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name="purchaseitem",
            name="created",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
# Generated by Django 4.2.3 on 2023-09-14 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Purchasing", "0007_goodsreceiptpoinfo_purchaseorder_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="goodsreceiptpoitem",
            name="lineNo",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="goodsreceiptpoitem",
            name="purchareOrderNo",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="purchaseitem",
            name="lineNo",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

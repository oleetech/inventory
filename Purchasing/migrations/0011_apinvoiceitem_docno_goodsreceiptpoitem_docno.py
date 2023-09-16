# Generated by Django 4.2.3 on 2023-09-16 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Purchasing", "0010_remove_goodsreceiptpoitem_purchaseorder_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="apinvoiceitem",
            name="docNo",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="goodsreceiptpoitem",
            name="docNo",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
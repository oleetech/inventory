# Generated by Django 4.2.3 on 2023-09-16 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Purchasing", "0009_purchaseitem_docno"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="goodsreceiptpoitem",
            name="purchaseOrder",
        ),
        migrations.AddField(
            model_name="apinvoiceinfo",
            name="goodsreReiptNo",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="apinvoiceitem",
            name="goodsreReiptNo",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="apinvoiceitem",
            name="lineNo",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

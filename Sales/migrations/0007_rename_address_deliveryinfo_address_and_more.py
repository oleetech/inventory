# Generated by Django 4.2.3 on 2023-08-30 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0006_salesquotetionitem_salesquotetioninfo"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="Address",
            new_name="address",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="Created",
            new_name="created",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="CustomerName",
            new_name="customerName",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="DocNo",
            new_name="docNo",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="SalesOrder",
            new_name="salesOrder",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="TotalAmount",
            new_name="totalAmount",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="TotalQty",
            new_name="totalQty",
        ),
        migrations.RenameField(
            model_name="deliveryitem",
            old_name="created_date",
            new_name="created",
        ),
        migrations.RenameField(
            model_name="deliveryitem",
            old_name="Delivery",
            new_name="delivery",
        ),
        migrations.RenameField(
            model_name="deliveryitem",
            old_name="Price",
            new_name="price",
        ),
        migrations.RenameField(
            model_name="deliveryitem",
            old_name="PriceTotal",
            new_name="priceTotal",
        ),
        migrations.RemoveField(
            model_name="deliveryinfo",
            name="created_date",
        ),
        migrations.RemoveField(
            model_name="deliveryitem",
            name="ItemName",
        ),
        migrations.RemoveField(
            model_name="deliveryitem",
            name="Quantity",
        ),
        migrations.AddField(
            model_name="deliveryitem",
            name="code",
            field=models.CharField(default="", max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="deliveryitem",
            name="name",
            field=models.CharField(default="", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="deliveryitem",
            name="uom",
            field=models.CharField(default="", max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="deliveryitem",
            name="quantity",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]

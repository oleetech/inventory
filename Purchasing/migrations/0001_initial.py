# Generated by Django 4.2.3 on 2023-08-30 06:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("BusinessPartners", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchaseOrderInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("docNo", models.PositiveIntegerField(default=1, unique=True)),
                ("address", models.CharField(blank=True, max_length=250)),
                ("created", models.DateField(default=django.utils.timezone.now)),
                (
                    "totalAmount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "totalQty",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "customerName",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="BusinessPartners.businesspartner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Purchase Order",
                "verbose_name_plural": "Purchase Order",
            },
        ),
        migrations.CreateModel(
            name="PurchaseItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(default="", max_length=20, null=True)),
                ("name", models.CharField(default="", max_length=100, null=True)),
                ("uom", models.CharField(default="", max_length=20, null=True)),
                (
                    "quantity",
                    models.DecimalField(decimal_places=4, default=0, max_digits=10),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "priceTotal",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Purchasing.purchaseorderinfo",
                    ),
                ),
            ],
        ),
    ]

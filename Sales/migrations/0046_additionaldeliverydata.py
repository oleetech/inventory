# Generated by Django 4.2.3 on 2023-09-13 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0045_deliveryinfo_challanreceiveddate_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdditionalDeliveryData",
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
                ("delivertobuyerdate", models.DateField()),
                (
                    "delivery_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Sales.deliveryinfo",
                    ),
                ),
            ],
        ),
    ]

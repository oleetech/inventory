# Generated by Django 4.2.3 on 2023-09-13 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0049_alter_challanreceiveddeliverydata_delivery_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionaldeliverydata",
            name="delivery_info",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="Sales.deliveryinfo"
            ),
        ),
    ]

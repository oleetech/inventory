# Generated by Django 4.2.3 on 2023-09-13 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0048_alter_additionaldeliverydata_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="challanreceiveddeliverydata",
            name="delivery_info",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="Sales.deliveryinfo"
            ),
        ),
    ]

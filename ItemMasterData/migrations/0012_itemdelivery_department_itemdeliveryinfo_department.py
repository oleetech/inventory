# Generated by Django 4.2.3 on 2023-09-06 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("GeneralSettings", "0003_department"),
        ("ItemMasterData", "0011_item_owner_itemdeliveryinfo_owner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="itemdelivery",
            name="department",
            field=models.CharField(default="1", max_length=50),
        ),
        migrations.AddField(
            model_name="itemdeliveryinfo",
            name="department",
            field=models.ForeignKey(
                blank=True,
                default=None,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="GeneralSettings.department",
            ),
        ),
    ]

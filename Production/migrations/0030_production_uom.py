# Generated by Django 4.2.3 on 2023-09-04 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0029_rename_created_date_production_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="production",
            name="uom",
            field=models.CharField(default="", max_length=100, null=True),
        ),
    ]
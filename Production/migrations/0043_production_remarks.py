# Generated by Django 4.2.3 on 2023-09-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0042_productioncomponent_docno"),
    ]

    operations = [
        migrations.AddField(
            model_name="production",
            name="remarks",
            field=models.CharField(blank=True, default="", max_length=250),
        ),
    ]

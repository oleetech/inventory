# Generated by Django 4.2.3 on 2023-09-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0041_productionreceiptitem_docno"),
    ]

    operations = [
        migrations.AddField(
            model_name="productioncomponent",
            name="docNo",
            field=models.PositiveIntegerField(default=1),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-03 02:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Production", "0026_alter_productionreceiptitem_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productionreceiptitem",
            name="created",
            field=models.DateField(default=datetime.date.today),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-13 02:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales", "0046_additionaldeliverydata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionaldeliverydata",
            name="delivertobuyerdate",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
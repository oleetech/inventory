# Generated by Django 4.2.4 on 2023-09-09 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0040_remove_productionreceiptitem_docno'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionreceiptitem',
            name='docNo',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

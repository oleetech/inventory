# Generated by Django 4.2.4 on 2023-08-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0019_remove_productionreceiptitem_docno'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionreceiptitem',
            name='lineNo',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

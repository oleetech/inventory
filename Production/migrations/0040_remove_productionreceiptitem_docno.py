# Generated by Django 4.2.4 on 2023-09-09 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0039_productionreceiptitem_docno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productionreceiptitem',
            name='docNo',
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-17 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0019_alter_issueforproductioninfo_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
    ]
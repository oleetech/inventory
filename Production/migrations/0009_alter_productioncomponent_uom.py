# Generated by Django 4.2.4 on 2023-08-29 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0008_alter_production_name_alter_productioncomponent_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productioncomponent',
            name='uom',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]

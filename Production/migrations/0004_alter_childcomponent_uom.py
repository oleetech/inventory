# Generated by Django 4.2.4 on 2023-08-25 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GeneralSettings', '0001_initial'),
        ('Production', '0003_alter_billofmaterials_name_alter_childcomponent_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childcomponent',
            name='uom',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='GeneralSettings.unit'),
        ),
    ]

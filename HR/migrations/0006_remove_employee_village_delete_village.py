# Generated by Django 4.2.4 on 2023-09-20 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0005_village_employee_village'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='village',
        ),
        migrations.DeleteModel(
            name='Village',
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-25 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billofmaterials',
            name='code',
        ),
        migrations.RemoveField(
            model_name='childcomponent',
            name='code',
        ),
    ]

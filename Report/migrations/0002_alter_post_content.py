# Generated by Django 4.2.4 on 2023-09-01 07:23

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
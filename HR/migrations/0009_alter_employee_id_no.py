# Generated by Django 4.2.4 on 2023-09-20 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0008_alter_employee_id_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id_no',
            field=models.IntegerField(max_length=10),
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-21 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0017_overtimerecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='employeeskill',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='employeeskill',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='employeeskill',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='policestation',
            name='district',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='district',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='police_station',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='EmployeeSkill',
        ),
        migrations.DeleteModel(
            name='PoliceStation',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]

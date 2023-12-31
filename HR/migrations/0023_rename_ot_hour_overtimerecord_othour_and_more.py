# Generated by Django 4.2.4 on 2023-09-25 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0022_attendance_holiday_marked_as_holiday_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='overtimerecord',
            old_name='ot_hour',
            new_name='othour',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave'), ('Holiday', 'Holiday')], default='Present', max_length=10),
        ),
    ]

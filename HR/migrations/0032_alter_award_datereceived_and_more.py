# Generated by Django 4.2.4 on 2023-09-26 16:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0031_alter_overtimerecord_othour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='dateReceived',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employeepromotion',
            name='promotion_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employeetraining',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='overtimerecord',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='pay_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='deadline',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
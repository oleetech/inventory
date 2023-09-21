# Generated by Django 4.2.4 on 2023-09-20 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0015_taskassignment_employeetraining_employeepromotion'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('device_id', models.CharField(max_length=20)),
                ('verification_type', models.CharField(max_length=20)),
                ('verification_code', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('work_code', models.CharField(max_length=20)),
                ('department_id', models.CharField(max_length=20)),
                ('shift_id', models.CharField(max_length=20)),
                ('late_arrival', models.BooleanField(default=False)),
                ('early_departure', models.BooleanField(default=False)),
                ('overtime', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('holiday', models.BooleanField(default=False)),
                ('leave_type', models.CharField(blank=True, max_length=20, null=True)),
                ('remarks', models.TextField(blank=True)),
                ('sync_status', models.CharField(max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HR.employee')),
            ],
        ),
    ]

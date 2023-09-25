# Generated by Django 4.2.4 on 2023-09-25 10:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0025_alter_attendance_date_alter_attendance_intime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resignation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resignation_date', models.DateField(default=django.utils.timezone.now)),
                ('reason', models.TextField(blank=True, null=True)),
                ('notice_period', models.PositiveIntegerField(default=30)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HR.employee')),
            ],
            options={
                'verbose_name': 'Resignation',
                'verbose_name_plural': 'Resignations',
            },
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('date', 'employee')},
        ),
        migrations.AlterUniqueTogether(
            name='employeetraining',
            unique_together={('date', 'employee')},
        ),
        migrations.AlterUniqueTogether(
            name='leaverequest',
            unique_together={('start_date', 'end_date', 'employee')},
        ),
        migrations.AlterUniqueTogether(
            name='overtimerecord',
            unique_together={('date', 'employee')},
        ),
        migrations.AlterUniqueTogether(
            name='payroll',
            unique_together={('pay_date', 'employee')},
        ),
        migrations.DeleteModel(
            name='AttendanceLog',
        ),
    ]

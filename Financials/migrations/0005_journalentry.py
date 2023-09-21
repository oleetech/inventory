# Generated by Django 4.2.4 on 2023-09-21 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Financials', '0004_delete_journalentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('debit', 'Debit'), ('credit', 'Credit')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=15)),
                ('date', models.DateField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Financials.chartofaccounts')),
            ],
        ),
    ]
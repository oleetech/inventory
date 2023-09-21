# Generated by Django 4.2.4 on 2023-09-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Purchasing', '0013_alter_apinvoiceinfo_totalqty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasequotetioninfo',
            name='totalAmount',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='purchasequotetionitem',
            name='quantity',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
        ),
    ]
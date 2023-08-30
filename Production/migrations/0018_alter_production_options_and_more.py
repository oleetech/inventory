# Generated by Django 4.2.4 on 2023-08-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0017_alter_productionreceiptitem_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='production',
            options={'verbose_name': ' Production Order', 'verbose_name_plural': 'Production Order'},
        ),
        migrations.AlterModelOptions(
            name='productionreceipt',
            options={'verbose_name': 'Receipt From Production', 'verbose_name_plural': 'Receipt From Production'},
        ),
        migrations.AddField(
            model_name='productionreceiptitem',
            name='docno',
            field=models.PositiveIntegerField(default=1, unique=True),
        ),
    ]
# Generated by Django 4.2.4 on 2023-08-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0004_alter_productionreceiptitem_itemname'),
    ]

    operations = [
        migrations.AddField(
            model_name='billofmaterials',
            name='code',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='childcomponent',
            name='code',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='billofmaterials',
            name='name',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]

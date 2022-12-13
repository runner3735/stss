# Generated by Django 3.2.15 on 2022-12-07 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_purchase_funding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='method',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Credit Card'), (2, 'Purchase Order'), (3, 'Invoice')], null=True),
        ),
    ]
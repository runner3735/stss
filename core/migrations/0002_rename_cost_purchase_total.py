# Generated by Django 3.2.15 on 2022-11-09 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='cost',
            new_name='total',
        ),
    ]

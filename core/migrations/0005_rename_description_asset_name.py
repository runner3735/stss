# Generated by Django 3.2.15 on 2022-10-04 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_asset_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='description',
            new_name='name',
        ),
    ]
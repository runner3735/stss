# Generated by Django 3.2.15 on 2022-12-16 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_person_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='acronym',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]

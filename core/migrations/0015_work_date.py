# Generated by Django 3.2.15 on 2023-08-24 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_job_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2.15 on 2022-12-14 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_purchase_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='purchaser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.person'),
        ),
    ]

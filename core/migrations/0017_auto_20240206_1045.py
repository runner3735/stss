# Generated by Django 3.2.15 on 2024-02-06 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_work_summary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ['-date']},
        ),
        migrations.CreateModel(
            name='PMI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last', models.DateField(blank=True, null=True)),
                ('frequency', models.IntegerField()),
                ('next', models.DateField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('details', models.TextField(blank=True, max_length=4096)),
                ('location', models.CharField(blank=True, max_length=128)),
                ('assets', models.ManyToManyField(editable=False, related_name='_core_pmi_assets_+', to='core.Asset')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.person')),
                ('customers', models.ManyToManyField(editable=False, related_name='_core_pmi_customers_+', to='core.Person')),
                ('departments', models.ManyToManyField(editable=False, related_name='_core_pmi_departments_+', to='core.Department')),
                ('rooms', models.ManyToManyField(editable=False, related_name='_core_pmi_rooms_+', to='core.Room')),
            ],
            options={
                'ordering': ['next'],
            },
        ),
    ]

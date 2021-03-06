# Generated by Django 3.0.4 on 2020-03-24 06:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0010_auto_20200324_0542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='name',
        ),
        migrations.AlterField(
            model_name='facility',
            name='address',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Address should be in proper format', regex='^\\d*[a-zA-Z][#.0-9a-zA-Z\\s,-]+$')]),
        ),
    ]

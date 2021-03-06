# Generated by Django 3.0.4 on 2020-03-24 05:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0007_auto_20200323_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Name should only consist of characters', regex='^(?i)[#.0-9a-zA-Z\\s,-]+$')])),
                ('address', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Address should be in proper format', regex='^(?i)[#.0-9a-zA-Z\\s,-]+$')])),
                ('medicare_ccn', models.IntegerField(unique=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='healthcare_app.City')),
            ],
        ),
    ]

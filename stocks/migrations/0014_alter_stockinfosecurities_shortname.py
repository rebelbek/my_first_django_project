# Generated by Django 5.1.4 on 2025-01-07 21:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0013_rename_changeable_stockinfosecurities_unchangeable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinfosecurities',
            name='shortname',
            field=models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]

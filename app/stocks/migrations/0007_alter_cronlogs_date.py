# Generated by Django 5.1.6 on 2025-02-17 05:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_cronlogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronlogs',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 17, 5, 9, 28, 991848, tzinfo=datetime.timezone.utc)),
        ),
    ]

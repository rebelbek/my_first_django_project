# Generated by Django 5.1.6 on 2025-03-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='last',
            field=models.FloatField(blank=True, default='', null=True),
        ),
    ]

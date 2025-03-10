# Generated by Django 5.1.6 on 2025-03-09 05:57

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CronLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func', models.CharField(max_length=40)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secid', models.CharField(max_length=10, unique=True)),
                ('boardid', models.CharField(max_length=40)),
                ('shortname', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(3)])),
                ('prevprice', models.FloatField(blank=True, default=0, null=True)),
                ('lotsize', models.IntegerField(blank=True, default=0)),
                ('facevalue', models.FloatField(blank=True, default=0, null=True)),
                ('boardname', models.CharField(max_length=40)),
                ('secname', models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(3)])),
                ('prevwaprice', models.FloatField(blank=True, default=0, null=True)),
                ('prevdate', models.DateField(blank=True, default=None, null=True)),
                ('issuesize', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('isin', models.CharField(max_length=40)),
                ('latname', models.CharField(max_length=40)),
                ('prevlegalcloseprice', models.FloatField(blank=True, default=0, null=True)),
                ('listlevel', models.IntegerField(blank=True, default=0, null=True)),
                ('settledate', models.DateField(blank=True, default=None, null=True)),
                ('open', models.FloatField(blank=True, default=0, null=True)),
                ('low', models.FloatField(blank=True, default=0, null=True)),
                ('high', models.FloatField(blank=True, default=0, null=True)),
                ('last', models.FloatField(blank=True, default=0, null=True)),
                ('value', models.FloatField(blank=True, default=0, null=True)),
                ('value_usd', models.FloatField(blank=True, default=0, null=True)),
                ('waprice', models.FloatField(blank=True, default=0, null=True)),
                ('valtoday', models.FloatField(blank=True, default=0, null=True)),
                ('valtoday_usd', models.FloatField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ['secid'],
            },
        ),
    ]

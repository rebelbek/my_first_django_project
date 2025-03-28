# Generated by Django 5.1.6 on 2025-03-09 05:57

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('is_receive_mail', models.BooleanField(default=False)),
                ('verification_uuid', models.UUIDField(default=uuid.uuid4, verbose_name='Unique Verification UUID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DealInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('buy_price', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('upper_border', models.FloatField(default=None, null=True)),
                ('lower_border', models.FloatField(default=None, null=True)),
                ('custom_name', models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(3)])),
                ('use_custom', models.BooleanField(default=False)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.stocks')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

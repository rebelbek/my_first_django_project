# Generated by Django 5.1.5 on 2025-01-27 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stocks',
            options={'ordering': ['secid']},
        ),
    ]

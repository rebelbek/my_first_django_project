# Generated by Django 5.1.4 on 2025-01-06 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_alter_stockinfo_boardid_alter_stockinfo_boardname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockinfo',
            name='last',
            field=models.FloatField(null=True),
        ),
    ]

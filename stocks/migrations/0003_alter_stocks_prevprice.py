# Generated by Django 5.1.5 on 2025-02-13 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_alter_stocks_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='prevprice',
            field=models.FloatField(null=True),
        ),
    ]

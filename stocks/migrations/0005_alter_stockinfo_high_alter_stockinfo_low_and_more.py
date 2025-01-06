# Generated by Django 5.1.4 on 2025-01-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_alter_stockinfo_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinfo',
            name='high',
            field=models.FloatField(default=0.1, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='low',
            field=models.FloatField(default=0.1, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='valtoday',
            field=models.FloatField(default=0.1, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='valtoday_usd',
            field=models.FloatField(default=0.1, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='value',
            field=models.FloatField(default=0.1, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='value_usd',
            field=models.FloatField(default=0.1, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='waprice',
            field=models.FloatField(default=0.1, null=True),
        ),
    ]

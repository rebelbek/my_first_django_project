# Generated by Django 5.1.4 on 2025-01-01 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_alter_stockinfo_issuesize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='secid',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_notificationuser_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationuser',
            name='date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

# Generated by Django 4.2.4 on 2024-05-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0002_djangoinfo_files_djangoinfo_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='djangolink',
            name='link',
            field=models.CharField(max_length=100),
        ),
    ]

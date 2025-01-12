# Generated by Django 5.1.4 on 2025-01-12 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTradeInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('secid', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('buy_price', models.IntegerField()),
                ('stocks', models.ManyToManyField(to='stocks.stockinfosecurities')),
            ],
        ),
    ]

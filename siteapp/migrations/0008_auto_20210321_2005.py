# Generated by Django 3.1.4 on 2021-03-21 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0007_auto_20210321_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='fei_h',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='temp_h',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='idata',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 20, 5, 29, 631799), primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 3.1.4 on 2021-03-21 17:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0006_auto_20210306_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idata',
            name='fei_hint',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='error_s',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='idata',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 17, 58, 37, 751414), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='idata',
            name='error_hint',
            field=models.CharField(default=0, max_length=50),
        ),
    ]

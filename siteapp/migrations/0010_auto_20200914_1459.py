# Generated by Django 3.1.1 on 2020-09-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0009_auto_20200914_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='ischecked',
            field=models.IntegerField(max_length=1),
        ),
    ]
# Generated by Django 3.1.1 on 2020-09-15 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0010_auto_20200914_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='ischecked',
            field=models.IntegerField(),
        ),
    ]
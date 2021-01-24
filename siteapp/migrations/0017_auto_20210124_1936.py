# Generated by Django 3.1.4 on 2021-01-24 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0016_auto_20210124_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='co2_b',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='info',
            name='co2_u',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='info',
            name='fei_b',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='info',
            name='fei_u',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='info',
            name='humi_b',
            field=models.DecimalField(decimal_places=1, default=50.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='info',
            name='humi_u',
            field=models.DecimalField(decimal_places=1, default=90.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='info',
            name='light_b',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='info',
            name='light_u',
            field=models.IntegerField(default=500),
        ),
        migrations.AlterField(
            model_name='info',
            name='temp_b',
            field=models.DecimalField(decimal_places=1, default=20.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='info',
            name='temp_u',
            field=models.DecimalField(decimal_places=1, default=25.0, max_digits=3),
        ),
    ]

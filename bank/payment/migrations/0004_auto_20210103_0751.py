# Generated by Django 3.1.3 on 2021-01-03 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20210103_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='account',
            field=models.FloatField(verbose_name='account'),
        ),
    ]

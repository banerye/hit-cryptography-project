# Generated by Django 3.1.3 on 2021-01-03 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210103_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='username'),
        ),
    ]

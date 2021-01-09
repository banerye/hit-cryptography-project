# Generated by Django 3.1.3 on 2021-01-03 07:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='dual_sign',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='dual_sign'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.TimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
    ]

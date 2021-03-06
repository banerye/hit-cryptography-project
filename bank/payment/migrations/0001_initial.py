# Generated by Django 3.1.3 on 2021-01-01 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='delete tag')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update time')),
                ('payer', models.CharField(max_length=20, verbose_name='payer')),
                ('payee', models.CharField(max_length=20, verbose_name='payee')),
                ('account', models.IntegerField(verbose_name='account')),
                ('timestamp', models.TimeField(verbose_name='timestamp')),
            ],
            options={
                'db_table': 's_payment',
            },
        ),
    ]

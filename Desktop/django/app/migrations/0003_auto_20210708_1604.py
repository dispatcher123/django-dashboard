# Generated by Django 3.2 on 2021-07-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_likes_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='total',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]

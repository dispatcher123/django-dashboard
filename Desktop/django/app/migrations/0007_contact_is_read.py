# Generated by Django 3.2 on 2021-07-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210708_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]

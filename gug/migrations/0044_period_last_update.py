# Generated by Django 2.0.7 on 2019-01-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gug', '0043_auto_20190102_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
    ]
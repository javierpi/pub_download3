# Generated by Django 2.0.7 on 2018-07-18 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gug', '0013_stats_id_dspace'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stats',
            unique_together={('google_service', 'period', 'id_dspace', 'publication')},
        ),
    ]

# Generated by Django 2.0.7 on 2019-01-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gug', '0040_dspace_workarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dspace',
            name='workarea',
        ),
        migrations.AddField(
            model_name='dspace',
            name='workarea',
            field=models.ManyToManyField(blank=True, related_name='workareas', to='gug.WorkArea'),
        ),
    ]

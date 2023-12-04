# Generated by Django 4.2.7 on 2023-12-04 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventmodel_event_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmodel',
            name='event_image',
        ),
        migrations.AddField(
            model_name='eventmodel',
            name='event_image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
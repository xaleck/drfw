# Generated by Django 5.1.4 on 2024-12-30 11:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_event_delete_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0013_media_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='media_type',
        ),
        migrations.RemoveField(
            model_name='media',
            name='source_type',
        ),
        migrations.RemoveField(
            model_name='media',
            name='storage_type',
        ),
    ]

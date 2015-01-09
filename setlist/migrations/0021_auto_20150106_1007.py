# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0020_auto_20150102_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setlistsectionsong',
            name='song_number',
            field=models.IntegerField(default=1, max_length=3),
        ),
    ]

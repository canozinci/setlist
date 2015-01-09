# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0021_auto_20150106_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setlistsectionsong',
            name='song_number',
            field=models.IntegerField(max_length=3),
        ),
        migrations.AlterUniqueTogether(
            name='setlistsectionsong',
            unique_together=None,
        ),
    ]

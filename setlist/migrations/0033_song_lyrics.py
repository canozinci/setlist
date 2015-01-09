# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0032_auto_20150107_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='lyrics',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

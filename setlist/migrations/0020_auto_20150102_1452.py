# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0019_auto_20150102_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='original_artist',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]

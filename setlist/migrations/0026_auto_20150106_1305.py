# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0025_auto_20150106_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='length',
            field=models.IntegerField(default=0),
        ),
    ]

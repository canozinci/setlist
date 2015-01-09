# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.date(2014, 12, 24), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.date(2014, 12, 24), auto_now=True),
            preserve_default=False,
        ),
    ]

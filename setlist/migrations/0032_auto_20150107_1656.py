# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0031_auto_20150107_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventattendance',
            name='status',
            field=models.NullBooleanField(default=None),
        ),
    ]

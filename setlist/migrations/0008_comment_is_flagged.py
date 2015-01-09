# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0007_auto_20141224_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_flagged',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

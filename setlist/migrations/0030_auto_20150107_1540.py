# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0029_auto_20150107_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='location',
            new_name='venue',
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(max_length=2, choices=[(b'PT', b'PRACTICE'), (b'CT', b'CONCERT'), (b'RC', b'RECORDING'), (b'PR', b'PR'), (b'OR', b'OTHER')]),
        ),
    ]

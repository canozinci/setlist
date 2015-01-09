# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0028_auto_20150107_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(max_length=2, choices=[(b'PT', b'REHEARSAL'), (b'CT', b'CONCERT'), (b'RC', b'RECORDING'), (b'PR', b'PR'), (b'OR', b'OTHER')]),
        ),
    ]

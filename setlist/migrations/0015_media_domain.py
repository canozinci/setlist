# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0014_auto_20141226_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='domain',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

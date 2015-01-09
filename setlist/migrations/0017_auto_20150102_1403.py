# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0016_auto_20141230_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='established_year',
            field=models.IntegerField(default=2015, max_length=4),
        ),
    ]

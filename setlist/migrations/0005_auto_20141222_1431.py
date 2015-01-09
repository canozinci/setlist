# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0004_auto_20141219_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setlist',
            name='band',
            field=models.ForeignKey(related_name=b'setlists', to='setlist.Band'),
        ),
    ]

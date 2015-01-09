# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0008_comment_is_flagged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinstrument',
            name='Instrument',
            field=models.ForeignKey(related_name=b'instrument', to='setlist.Instrument'),
        ),
    ]

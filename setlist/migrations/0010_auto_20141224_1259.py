# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0009_auto_20141224_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songpart',
            name='user_instrument',
            field=models.ForeignKey(related_name=b'user_instrument', to='setlist.UserInstrument'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0010_auto_20141224_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinstrument',
            name='user',
            field=models.ForeignKey(related_name=b'user_playing', to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import setlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(max_length=500, null=True, upload_to=setlist.models._image_upload_path, blank=True),
            preserve_default=True,
        ),
    ]

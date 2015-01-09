# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import setlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0002_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='logo',
            field=models.ImageField(null=True, upload_to=setlist.models._image_upload_path, blank=True),
        ),
    ]

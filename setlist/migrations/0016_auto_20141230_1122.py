# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0015_media_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='setlistsectionsong',
            name='setlist',
            field=models.ForeignKey(related_name=b'setlist_section_songs', default=1, to='setlist.Setlist'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='setlistsection',
            name='setlist',
            field=models.ForeignKey(related_name=b'sections', to='setlist.Setlist'),
        ),
        migrations.AlterField(
            model_name='setlistsectionsong',
            name='section',
            field=models.ForeignKey(related_name=b'section_songs', to='setlist.SetlistSection'),
        ),
        migrations.AlterField(
            model_name='setlistsectionsong',
            name='song',
            field=models.ForeignKey(related_name=b'setlist_sections', to='setlist.Song'),
        ),
    ]

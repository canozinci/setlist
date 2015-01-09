# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0030_auto_20150107_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=None)),
                ('bandmember', models.ForeignKey(related_name=b'attending', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(related_name=b'attending', to='setlist.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='CalendarEvent',
        ),
        migrations.DeleteModel(
            name='Concert',
        ),
        migrations.DeleteModel(
            name='ExternalMedia',
        ),
        migrations.DeleteModel(
            name='SongExternalMedia',
        ),
        migrations.DeleteModel(
            name='SongPartExternalMedia',
        ),
    ]

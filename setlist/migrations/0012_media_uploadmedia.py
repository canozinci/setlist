# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('setlist', '0011_auto_20141224_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.TextField()),
                ('source_type', models.CharField(max_length=1, choices=[(0, b'OWN'), (1, b'EXTERNAL')])),
                ('media_type', models.CharField(max_length=1, choices=[(0, b'VIDEO'), (1, b'AUDIO'), (2, b'HTML'), (2, b'IMAGE')])),
                ('storage_type', models.CharField(max_length=1, choices=[(0, b'OWN'), (1, b'EXTERNAL')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('file_creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

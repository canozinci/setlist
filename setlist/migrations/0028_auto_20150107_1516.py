# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0027_auto_20150106_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('type', models.CharField(max_length=1, choices=[(0, b'REHEARSAL'), (1, b'CONCERT'), (2, b'RECORDING'), (3, b'PR'), (4, b'OTHER')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('band', models.ForeignKey(related_name=b'events', to='setlist.Band')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('adress', models.CharField(max_length=400, null=True, blank=True)),
                ('city', models.CharField(max_length=200, null=True, blank=True)),
                ('state', models.CharField(max_length=2, null=True, blank=True)),
                ('country', models.CharField(max_length=200, null=True, blank=True)),
                ('contact_person_name', models.CharField(max_length=200, null=True, blank=True)),
                ('phone', models.CharField(max_length=200, null=True, blank=True)),
                ('homepage', models.CharField(max_length=200, null=True, blank=True)),
                ('twitter_username', models.CharField(max_length=200, null=True, blank=True)),
                ('instagram_username', models.CharField(max_length=200, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Rehearsal',
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(related_name=b'events', to='setlist.Venue'),
            preserve_default=True,
        ),
    ]

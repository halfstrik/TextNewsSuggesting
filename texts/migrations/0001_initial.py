# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommonTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('associations', models.CharField(max_length=1024)),
            ],
            options={
                'verbose_name': 'Common tag',
                'verbose_name_plural': 'Common tags',
            },
        ),
        migrations.CreateModel(
            name='CommonTaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('weigh', models.CharField(default=b'AV', max_length=2,
                                           choices=[(b'WK', b'Weak'), (b'AV', b'Average'), (b'ST', b'Strong')])),
                ('content_type',
                 models.ForeignKey(related_name='texts_commontaggeditem_tagged_items', verbose_name='Content type',
                                   to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='texts_commontaggeditem_items', to='texts.CommonTag')),
            ],
            options={
                'verbose_name': 'Common Tagged Item',
                'verbose_name_plural': 'Common Tagged Items',
            },
        ),
        migrations.CreateModel(
            name='CommonTagRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weigh', models.CharField(default=b'AV', max_length=2,
                                           choices=[(b'WK', b'Weak'), (b'AV', b'Average'), (b'ST', b'Strong')])),
                ('first_tag', models.ForeignKey(related_name='first_tag', to='texts.CommonTag')),
                ('second_tag', models.ForeignKey(related_name='second_tag', to='texts.CommonTag')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyFirst',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PropertySecond',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('feed_link', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SourceTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('source', models.ForeignKey(to='texts.Source')),
            ],
            options={
                'verbose_name': 'Source tag',
                'verbose_name_plural': 'Source tags',
            },
        ),
        migrations.CreateModel(
            name='SourceTaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type',
                 models.ForeignKey(related_name='texts_sourcetaggeditem_tagged_items', verbose_name='Content type',
                                   to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='texts_sourcetaggeditem_items', to='texts.SourceTag')),
            ],
            options={
                'verbose_name': 'Source Tagged Item',
                'verbose_name_plural': 'Source Tagged Items',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('link', models.CharField(max_length=512, null=True, blank=True)),
                ('published', models.DateTimeField(null=True, blank=True)),
                ('days_to_life', models.IntegerField(default=1)),
                ('keywords', models.CharField(max_length=255, null=True, blank=True)),
                ('is_moderated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('property_first', models.ForeignKey(blank=True, to='texts.PropertyFirst', null=True)),
                ('property_second', models.ForeignKey(blank=True, to='texts.PropertySecond', null=True)),
                ('source', models.ForeignKey(to='texts.Source')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(editable=False, to='texts.Text'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='commontagrelationship',
            unique_together=set([('first_tag', 'second_tag')]),
        ),
    ]

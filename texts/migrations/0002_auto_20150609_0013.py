# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('texts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyNormalizedWords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('words', models.CharField(max_length=255)),
                ('tag', models.ForeignKey(to='texts.CommonTag')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='keynormalizedwords',
            unique_together=set([('words', 'tag')]),
        ),
    ]

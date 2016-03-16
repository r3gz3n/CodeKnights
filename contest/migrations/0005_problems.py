# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_delete_problems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problemId', models.CharField(max_length=50)),
                ('problemTitle', models.CharField(max_length=50)),
                ('problemPath', models.FilePathField(path=b'/home/r3gz3n/CodeKnights/problems', allow_folders=True)),
            ],
        ),
    ]

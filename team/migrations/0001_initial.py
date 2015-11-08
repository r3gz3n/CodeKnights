# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeamDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamName', models.CharField(max_length=20)),
                ('member1Name', models.CharField(max_length=50)),
                ('member1Branch', models.CharField(max_length=50)),
                ('member1Year', models.IntegerField(default=0)),
                ('member1Email', models.EmailField(max_length=50)),
                ('member1Phone', models.CharField(max_length=10)),
                ('member1College', models.CharField(max_length=50)),
                ('member2Name', models.CharField(max_length=50)),
                ('member2Branch', models.CharField(max_length=50)),
                ('member2Year', models.IntegerField(default=0)),
                ('member3Name', models.CharField(max_length=50)),
                ('member3Branch', models.CharField(max_length=50)),
                ('member3Year', models.IntegerField(default=0)),
            ],
        ),
    ]

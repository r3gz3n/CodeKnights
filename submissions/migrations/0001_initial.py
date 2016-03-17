# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamName', models.CharField(max_length=20)),
                ('submissionTime', models.DateTimeField()),
                ('solution', models.FileField(upload_to=b'/home/r3gz3n/CodeKnights/allSubmissions')),
                ('problemId', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=10)),
                ('verdict', models.CharField(max_length=50)),
                ('timeTaken', models.FloatField()),
                ('memoryTaken', models.FloatField()),
            ],
        ),
    ]

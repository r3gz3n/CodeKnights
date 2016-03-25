# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0003_submissions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Submissions',
        ),
    ]

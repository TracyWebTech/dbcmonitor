# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 4, 24, 12, 54, 14, 13274, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
    ]

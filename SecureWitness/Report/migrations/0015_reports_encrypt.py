# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0014_auto_20150415_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='encrypt',
            field=models.BooleanField(default=False),
        ),
    ]

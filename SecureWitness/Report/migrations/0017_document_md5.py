# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0016_reports_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='md5',
            field=models.CharField(max_length=32, null=True),
        ),
    ]

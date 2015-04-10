# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0007_remove_reports_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reports',
            name='file',
        ),
        migrations.AddField(
            model_name='document',
            name='report',
            field=models.ForeignKey(to='Report.reports', default=None),
            preserve_default=False,
        ),
    ]

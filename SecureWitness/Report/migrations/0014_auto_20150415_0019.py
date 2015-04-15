# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0013_auto_20150413_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='folder',
            field=models.ForeignKey(related_name='reports_set', default=None, null=True, to='Report.Folder'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0008_auto_20150403_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='report',
            field=models.ForeignKey(null=True, to='Report.reports'),
            preserve_default=True,
        ),
    ]

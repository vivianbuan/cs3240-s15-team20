# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0012_auto_20150413_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(to='accounts.UserProfile', related_name='folder_set', default=None, null=True),
            preserve_default=True,
        ),
    ]

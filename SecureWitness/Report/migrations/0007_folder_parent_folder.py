# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0006_auto_20150401_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='parent_folder',
            field=models.ForeignKey(default=1, to='Report.Folder'),
            preserve_default=True,
        ),
    ]

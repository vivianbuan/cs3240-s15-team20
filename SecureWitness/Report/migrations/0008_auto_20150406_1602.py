# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0007_folder_parent_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parent_folder',
            field=models.ForeignKey(default=None, null=True, to='Report.Folder', related_name='parents'),
            preserve_default=True,
        ),
    ]

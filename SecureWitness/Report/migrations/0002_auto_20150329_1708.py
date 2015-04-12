# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='report',
        ),
        migrations.AddField(
            model_name='reports',
            name='folder',
            field=models.ForeignKey(default=1, to='Report.Folder'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='file_name',
            field=models.CharField(default='DEFAULT FOLDER', max_length=30),
            preserve_default=True,
        ),
    ]

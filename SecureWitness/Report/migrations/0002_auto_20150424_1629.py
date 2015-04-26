# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='md5',
            field=models.CharField(default='', max_length=32, null=True),
            preserve_default=True,
        ),
    ]

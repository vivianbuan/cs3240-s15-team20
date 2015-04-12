# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_administrator'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='suspended',
            field=models.BooleanField(default=0),
            preserve_default=True,
        ),
    ]

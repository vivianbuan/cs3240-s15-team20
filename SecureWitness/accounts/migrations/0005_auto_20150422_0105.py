# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150422_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='suspended',
            field=models.BooleanField(default=1),
            preserve_default=True,
        ),
    ]

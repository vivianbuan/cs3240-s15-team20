# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SiteMail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='date',
            field=models.DateTimeField(null=True, auto_now_add=True, default=None),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('Report', '0015_reports_encrypt'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
    ]

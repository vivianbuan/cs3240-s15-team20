# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0011_folder_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(related_name='folder_set', to='accounts.UserProfile', default=None),
            preserve_default=True,
        ),
    ]

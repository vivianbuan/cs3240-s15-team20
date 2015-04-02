# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0003_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reports',
            old_name='bodytext',
            new_name='details',
        ),
        migrations.AddField(
            model_name='reports',
            name='date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reports',
            name='file',
            field=models.FileField(upload_to='documents/%Y/%m/%d', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reports',
            name='keywords',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reports',
            name='location',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reports',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reports',
            name='short',
            field=models.TextField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reports',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]

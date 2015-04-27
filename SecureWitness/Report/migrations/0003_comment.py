# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0002_auto_20150424_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('text', models.TextField()),
                ('report', models.ForeignKey(to='Report.reports')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_suspended'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.TextField(default='No Title', max_length=30)),
                ('details', models.TextField()),
                ('from_user', models.ForeignKey(null=True, to='accounts.UserProfile', related_name='sent_mails', default=None)),
                ('to_user', models.ForeignKey(null=True, to='accounts.UserProfile', related_name='receive_mails', default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

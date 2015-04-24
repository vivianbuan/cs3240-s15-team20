# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('accounts', '0008_auto_20150424_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('md5', models.CharField(null=True, max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file_name', models.CharField(max_length=30, default='DEFAULT FOLDER')),
                ('owner', models.ForeignKey(null=True, to='accounts.UserProfile', default=None, related_name='folder_set')),
                ('parent_folder', models.ForeignKey(null=True, to='Report.Folder', default=None, related_name='parents')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='reports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('author', models.CharField(max_length=30)),
                ('short', models.TextField(max_length=100)),
                ('details', models.TextField()),
                ('location', models.CharField(null=True, max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('keywords', models.CharField(null=True, max_length=100)),
                ('private', models.BooleanField(default=False)),
                ('encrypt', models.BooleanField(default=False)),
                ('folder', models.ForeignKey(null=True, to='Report.Folder', default=None, related_name='reports_set')),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='document',
            name='report',
            field=models.ForeignKey(null=True, to='Report.reports'),
            preserve_default=True,
        ),
    ]

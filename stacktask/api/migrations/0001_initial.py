# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
import stacktask.api.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', jsonfield.fields.JSONField(default={})),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('acknowledged', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('uuid', models.CharField(default=stacktask.api.models.hex_uuid, max_length=200, serialize=False, primary_key=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('keystone_user', jsonfield.fields.JSONField(default={})),
                ('action_view', models.CharField(max_length=200)),
                ('action_notes', jsonfield.fields.JSONField(default={})),
                ('cancelled', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_on', models.DateTimeField(null=True)),
                ('completed_on', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expires', models.DateTimeField()),
                ('task', models.ForeignKey(to='api.Task')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='task',
            field=models.ForeignKey(to='api.Task'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 15:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0022_auto_20161112_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usercreatedevent',
            name='eventDate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='allEvent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CompleteOrSharedInfo', to='mainApi.AllEvent'),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='dateCompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='dateShared',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='userProfile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
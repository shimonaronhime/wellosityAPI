# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0029_auto_20161126_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='dateCompleted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='dateShared',
            field=models.DateField(blank=True, null=True),
        ),
    ]
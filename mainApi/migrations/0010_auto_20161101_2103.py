# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0009_auto_20161101_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ('user',)},
        ),
    ]
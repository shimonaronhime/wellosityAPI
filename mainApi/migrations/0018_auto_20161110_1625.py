# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0017_auto_20161107_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='allEvents',
            field=models.ManyToManyField(blank=True, null=True, related_name='allEvents', through='mainApi.UserEvent', to='mainApi.AllEvent'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

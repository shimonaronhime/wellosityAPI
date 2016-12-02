# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0003_auto_20161030_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermedhistories',
            name='allMedHistories',
        ),
        migrations.RemoveField(
            model_name='usermedhistories',
            name='userProfiles',
        ),
        migrations.RenameField(
            model_name='userprofiles',
            old_name='image',
            new_name='profilePicture',
        ),
        migrations.AddField(
            model_name='allevents',
            name='profile',
            field=models.ManyToManyField(through='mainApi.UserEvents', to='mainApi.UserProfiles'),
        ),
        migrations.AddField(
            model_name='allmedhistories',
            name='profile',
            field=models.ManyToManyField(to='mainApi.UserProfiles'),
        ),
        migrations.DeleteModel(
            name='UserMedHistories',
        ),
    ]
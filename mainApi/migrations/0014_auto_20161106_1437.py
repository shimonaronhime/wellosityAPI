# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0013_auto_20161106_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='userEvents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventComments', to='mainApi.UserEvent'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='userProfiles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApi.UserProfile'),
        ),
    ]
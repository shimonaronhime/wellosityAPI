# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 14:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApi', '0021_auto_20161112_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercreatedevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userCreatedEvent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventsOfUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
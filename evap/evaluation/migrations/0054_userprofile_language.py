# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-26 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0053_create_cronjob_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='language'),
        ),
    ]

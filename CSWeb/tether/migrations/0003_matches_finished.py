# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-21 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tether', '0002_matches_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]

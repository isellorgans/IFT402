# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-28 02:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tether', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('player1', models.CharField(max_length=255)),
                ('player2', models.CharField(max_length=255)),
                ('player3', models.CharField(max_length=255)),
                ('player4', models.CharField(max_length=255)),
                ('player5', models.CharField(max_length=255)),
                ('player6', models.CharField(max_length=255)),
                ('player7', models.CharField(max_length=255)),
                ('player8', models.CharField(max_length=255)),
                ('player9', models.CharField(max_length=255)),
                ('player10', models.CharField(max_length=255)),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tether.League')),
            ],
        ),
    ]
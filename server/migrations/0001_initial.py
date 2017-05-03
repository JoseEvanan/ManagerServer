# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_server', models.CharField(blank=True, max_length=1, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
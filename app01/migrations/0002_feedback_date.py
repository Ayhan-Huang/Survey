# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='日期'),
        ),
    ]
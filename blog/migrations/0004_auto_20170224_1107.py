# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170224_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes_num',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes_num',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

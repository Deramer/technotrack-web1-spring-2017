# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-22 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20170416_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]

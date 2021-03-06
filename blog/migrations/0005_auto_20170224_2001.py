# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170224_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments_tree',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='comments_tree',
            name='next_id',
        ),
        migrations.RemoveField(
            model_name='comments_tree',
            name='prev_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='next_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='prev_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Comment'),
        ),
        migrations.DeleteModel(
            name='Comments_tree',
        ),
    ]

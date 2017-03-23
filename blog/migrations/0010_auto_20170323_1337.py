# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170322_1733'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments_likes',
            new_name='CommentsLikes',
        ),
        migrations.RenameModel(
            old_name='Posts_likes',
            new_name='PostsLikes',
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Root comment'), (1, 'Usual comment'), (2, 'Deleted comment'), (3, 'Downvoted comment')], default=1),
        ),
    ]

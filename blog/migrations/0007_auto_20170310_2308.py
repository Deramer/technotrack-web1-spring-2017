# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 23:08
from __future__ import unicode_literals
from html import unescape

from django.db import migrations
from django.utils.html import escape


def my_unescape(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Comment = apps.get_model('blog', 'Comment')
    for post in Post.objects.all():
        post.text = unescape(post.text.replace('<br>', '\n'))
        post.save()
    for comment in Comment.objects.all():
        comment.text = unescape(comment.text.replace('<br>', '\n'))
        comment.save()

def reciprocal(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Comment = apps.get_model('blog', 'Comment')
    for post in Post.objects.all():
        post.text = escape(post.text).replace('\n', '<br>')
        post.save()
    for comment in Comment.objects.all():
        comment.text = escape(comment.text).replace('\n', '<br>')
        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170305_1336'),
    ]

    operations = [
            migrations.RunPython(my_unescape, reverse_code=reciprocal)
    ]

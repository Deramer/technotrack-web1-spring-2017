from django.db import models
from django.conf import settings


class Blog(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Post(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_num = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes_num = models.IntegerField(blank=True, default=0)
    prev_id = models.ForeignKey('self', models.CASCADE, null=True, blank=True, related_name='+')
    next_id = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, related_name='+')
    
    def __str__(self):
        return self.text


class Posts_likes(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)


class Comments_likes(models.Model):
    comment = models.ForeignKey(Comment, models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

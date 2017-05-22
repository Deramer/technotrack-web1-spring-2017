from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey

from blog.managers import PostQuerySet


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Categories'


class Blog(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return str(self.title)


class GenericLike(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    LIKE_STATUS = 1
    DISLIKE_STATUS = -1
    STATUS_CHOICES = (
            (DISLIKE_STATUS, 'Dislike'),
            (LIKE_STATUS, 'Like'),
    )
    status = models.IntegerField(blank=True, default=LIKE_STATUS, choices=STATUS_CHOICES)


class Post(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_num = models.IntegerField(blank=True, default=0)
    likes = GenericRelation(GenericLike)
    is_published = models.BooleanField(default=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def update_likes_num(self):
        self.likes_num = self.likes.aggregate(models.Sum('status'))['status__sum']
        self.save()


class Comment(MPTTModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes_num = models.IntegerField(blank=True, default=0)
    likes = GenericRelation(GenericLike)
    post = models.ForeignKey(Post, models.CASCADE)
    USUAL_COMMENT = 1
    DELETED_COMMENT = 2
    DOWNVOTED_COMMENT = 3
    DOWNVOTED_EDGE = -2
    STATUS_CHOICES = (
            (USUAL_COMMENT, 'Usual comment'), 
            (DELETED_COMMENT, 'Deleted comment'),
            (DOWNVOTED_COMMENT, 'Downvoted comment'),
    )
    status = models.IntegerField(blank=True, default=USUAL_COMMENT, choices=STATUS_CHOICES)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.text

    def update_likes_num(self):
        if self.status != self.DELETED_COMMENT:
            self.likes_num = self.likes.aggregate(models.Sum('status'))['status__sum']
            if self.likes_num <= self.DOWNVOTED_EDGE:
                self.status = self.DOWNVOTED_COMMENT
            else:
                self.status = self.USUAL_COMMENT
        self.save()

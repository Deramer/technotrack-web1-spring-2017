from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


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


class Comment(MPTTModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes_num = models.IntegerField(blank=True, default=0)
    ROOT_COMMENT = 0
    USUAL_COMMENT = 1
    DELETED_COMMENT = 2
    DOWNVOTED_COMMENT = 3
    DOWNVOTED_EDGE = -2
    STATUS_CHOICES = (
            (ROOT_COMMENT, 'Root comment'),
            (USUAL_COMMENT, 'Usual comment'), 
            (DELETED_COMMENT, 'Deleted comment'),
            (DOWNVOTED_COMMENT, 'Downvoted comment'),
    )
    status = models.IntegerField(blank=True, default=USUAL_COMMENT, choices=STATUS_CHOICES)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.text

    def update_likes_num(self):
        if self.status == self.ROOT_COMMENT:
            self.likes_num = CommentsLikes.objects.filter(comment=self.id).aggregate(models.Sum('status'))['status__sum']
        if self.status != self.ROOT_COMMENT and self.status != self.DELETED_COMMENT:
            self.likes_num = CommentsLikes.objects.filter(comment=self.id).aggregate(models.Sum('status'))['status__sum']
            if self.likes_num <= self.DOWNVOTED_EDGE:
                self.status = self.DOWNVOTED_COMMENT
            else:
                self.status = self.USUAL_COMMENT
        self.save()


class Post(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_num = models.IntegerField(blank=True, default=0)
    comments = models.ForeignKey(Comment, models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class CommentsLikes(models.Model):
    comment = models.ForeignKey(Comment, models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    LIKE_STATUS = 1
    DISLIKE_STATUS = -1
    STATUS_CHOICES = (
            (DISLIKE_STATUS, 'Dislike'),
            (LIKE_STATUS, 'Like'),
    )
    status = models.IntegerField(blank=True, default=LIKE_STATUS, choices=STATUS_CHOICES)

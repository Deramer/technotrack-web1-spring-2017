from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

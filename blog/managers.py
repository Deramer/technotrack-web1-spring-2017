from django.db import models
from django.db.models import Q

class PostQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(Q(creator = user.id) | Q(is_published = True))

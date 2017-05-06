from django.db import models

# Create your models here.

class Translation(models.Model):
    translation = models.CharField(max_length=255)

class Word(models.Model):
    set_num = models.IntegerField()
    word = models.CharField(max_length=255)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    synonims = models.ManyToManyField('self')

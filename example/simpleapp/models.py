from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class SimpleText(models.Model):
    """A Testing app"""
    firstname = models.CharField(blank=True, max_length=255)
    lastname = models.CharField(blank=True, max_length=255)
    favorite_color = models.CharField(blank=True, max_length=255)
    
    def __unicode__(self):
        return self.firstname


class SimpleCategory(models.Model):
    """Another Testing app"""
    name = models.CharField(max_length=255)
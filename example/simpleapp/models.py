from django.db import models

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
import datetime
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class DummyEntry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    publish_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.title
        
        
class DummyBookmark(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=200)
    
    
class DummyVideo(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=200)
    
    
class DummyImage(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=200)
    

class RelatedContent(models.Model):
    entry = models.ForeignKey(DummyEntry)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    add_date = models.DateTimeField(default=datetime.datetime.now)
    
   
   
def get_or_create_example():
    bm_ctype = ContentType.objects.get_for_model(DummyBookmark)
    vi_ctype = ContentType.objects.get_for_model(DummyVideo)
    im_ctype = ContentType.objects.get_for_model(DummyImage)
    en_ctype = ContentType.objects.get_for_model(DummyEntry)

    entry, cr = DummyEntry.objects.get_or_create(
        title="This is an example entry",
        body="This is only an example entry",
        author="John Smith")
        
    bm1, cr = DummyBookmark.objects.get_or_create(
        url="http://google.com",
        name="Google")
       
    bm2, cr = DummyBookmark.objects.get_or_create(
        url="http://djangoproject.com",
        name="Django Web Framework")
        
    vid1, cr = DummyVideo.objects.get_or_create(
        url="http://www.youtube.com/watch?v=K24mFGlJij0&playnext=1&list=PL4A64BDBA5F9629AE",
        name="Django's Caravan - Gypsy Jazz Guitar - Leigh Jackson") 
        
    vid2, cr = DummyVideo.objects.get_or_create(
        url="http://www.youtube.com/watch?v=_cZfMLVdvxI&feature=related",
        name="\"All Of Me,\" gypsy jazz style")
        
    img1, cr = DummyImage.objects.get_or_create(
        url="http://www.flickr.com/photos/alisonlyons/5678882139/",
        name="Fair Exchange From alison lyons photography")

    img2, cr = DummyImage.objects.get_or_create(
        url="http://www.flickr.com/photos/amury/5683581351/",
        name="Pray for Japan. From kaneko_ryo")
        
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=bm_ctype,
        object_id=bm1.pk)
        
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=bm_ctype,
        object_id=bm2.pk)
    
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=vi_ctype,
        object_id=vid1.pk)
    
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=vi_ctype,
        object_id=vid2.pk)
    
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=im_ctype,
        object_id=img1.pk)
    
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=im_ctype,
        object_id=img2.pk)
   
    RelatedContent.objects.get_or_create(
        entry=entry,
        content_type=en_ctype,
        object_id=entry.pk)
        
    return {'entry': entry,
            'related_content': RelatedContent.objects.all()}
     

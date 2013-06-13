from django.db import models

class User(models.Model):
    ''' An admin user '''
    user_name = models.CharField(max_length=255)
    user_login = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    user_deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user_name
    
class LifeStream(models.Model):
    ls_title = models.CharField(max_length=128)
    ls_tagline = models.TextField(null=True, blank=True)
    ls_baseurl = models.CharField(max_length=1000)
    ls_user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.ls_title
    
class Feed(models.Model):
    feed_lifestream = models.ForeignKey(LifeStream)
    feed_name = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=1000)
    feed_domain = models.CharField(max_length=255)
    feed_deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.feed_name

class Tag(models.Model):
    tag_sluf = models.CharField(max_length=50, primary_key=True)
    tag_name = models.CharField(max_length=30)
    tag_count = models.IntegerField()
    tag_deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.tag_name
    
class Item(models.Model):
    item_feed = models.ForeignKey(Feed)
    item_date = models.DateTimeField()
    item_title = models.CharField(max_length=255)
    item_content = models.TextField(null=True, blank=True)
    item_clean_content = models.TextField(null=True, blank=True)
    item_author = models.CharField(max_length=255, null=True, blank=True)
    item_permalink = models.CharField(max_length=1000)
    item_tags = models.ManyToManyField(Tag, null=True, blank=True)
    item_published = models.BooleanField(default=True)
    item_deleted = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.item_title
        
from django.db import models
from datetime import datetime

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    author = models.ForeignKey('auth.User')
    items = models.ManyToManyField('cat.MuseumObject', related_name='items', blank=True)

    is_published = models.BooleanField()
    categories = models.CharField(max_length=120, blank=True)
    rights = models.CharField(max_length=200,
            help_text="Information about rights held in and over the entity")
    access_rights = models.CharField(max_length=200,
            help_text="Information about who can access the entity, including access restrictions based on privacy, security, or other policies.")
    edit_url = models.URLField(verify_exists=False, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    last_published = models.DateTimeField(blank=True, null=True)
    date_published = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published:
            if not self.date_published:
                self.date_published = datetime.now()
            self.last_published = datetime.now()
        super(Collection, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('collection_detail', [str(self.id)])

    def entry_attributes(self):
        return {u"xmlns": u"http://www.w3.org/2005/Atom",
                u"xmlns:rdfa": u"http://www.w3.org/ns/rdfa#"}


class Exhibition(Collection):
    start_date = models.DateField()
    end_date = models.DateField()

class Syndication(models.Model):
   remote_url = models.CharField(max_length=300) 

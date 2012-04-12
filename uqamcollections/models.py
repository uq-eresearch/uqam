from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
import requests


class Collection(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    author = models.ForeignKey('auth.User', null=True, blank=True)
    items = models.ManyToManyField('cat.MuseumObject',
            related_name='collections', blank=True)

    is_public = models.BooleanField(
            help_text="Should collection be visible to the public")
    is_syndicated = models.BooleanField(
            help_text="Should collection be sent for syndication")
    categories = models.CharField(max_length=120, blank=True)
    rights = models.CharField(max_length=200,
            help_text="Information about rights held in and over the entity")
    access_rights = models.CharField(max_length=200,
            help_text="Information about who can access the entity, "
            "including access restrictions based on privacy, security, "
            "or other policies.")

    updated = models.DateTimeField(auto_now=True, editable=False,
            help_text="Date the collection was last edited")
    created = models.DateTimeField(auto_now_add=True, editable=False,
            help_text="Date the collection was initially created")

    edit_url = models.URLField(verify_exists=False, blank=True, editable=False,
            help_text="Remotely assigned URL for updating syndicated data")
    last_published = models.DateTimeField(blank=True, null=True,
            editable=False, help_text="Date the collection was last published,"
            " or edited while published")
    date_published = models.DateTimeField(blank=True, null=True,
            editable=False,
            help_text="Date the collection was first published")

    last_syndicated = models.DateTimeField(blank=True, null=True,
            editable=False,
            help_text="Date the collection was first sent for syndication")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_public:
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


class Syndication(models.Model):
    remote_url = models.CharField(max_length=300)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    def syndicate_collection(collection):
        return "do something"

    def __unicode__(self):
        return self.remote_url

from tasks import send_collection


def queue_for_syndication(sender, **kwargs):
    collection = kwargs['instance']
    syn = Syndication.objects.get(id=1)
    post_save.disconnect(queue_for_syndication, sender=Collection)

    kwargs['instance'].save()

    post_save.connect(queue_for_syndication, sender=Collection)

#post_save.connect(queue_for_syndication, sender=Collection)

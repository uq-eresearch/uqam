from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from cat.models import Category
from location.models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from django.utils.xmlutils import SimplerXMLGenerator
from django.conf import settings
from utils.utils import get_site_url
import StringIO
from django.contrib.sites.models import Site
from django.utils.feedgenerator import rfc3339_date


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
                u"xmlns:rdfa": u"http://www.w3.org/ns/rdfa#",
                u"xmlns:georss": u"http://www.georss.org/georss"}

    def get_categories(self):
        """Queryset of categories of items in collection"""
        items = self.items.all()
        return Category.objects.filter(
            museumobject__in=items).distinct()

    def get_places(self):
        """
        Get all places referenced by items in this collection
        """
        items = self.items.all()
        places = []
        for place_type in (GlobalRegion, Country, StateProvince, RegionDistrict, Locality):
            places.extend(place_type.objects.filter(museumobject__in=items).distinct())
        return places


class Syndication(models.Model):
    remote_url = models.CharField(max_length=300)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    def syndicate_collection(collection):
        return "do something"

    def __unicode__(self):
        return self.remote_url


def queue_for_syndication(sender, **kwargs):
    collection = kwargs['instance']
    syn = Syndication.objects.get(id=1)
    post_save.disconnect(queue_for_syndication, sender=Collection)

    kwargs['instance'].save()

    post_save.connect(queue_for_syndication, sender=Collection)

#post_save.connect(queue_for_syndication, sender=Collection)

import requests


def syndicate_collection(collection, server):
    atom = collection_as_atom(collection)
    server_url = "http://dataspace-uat.metadata.net/"
    login_url = server_url + "login"
    collections_url = server_url + "collections"
    login_data = {'username': server.username,
                  'password': server.password}
    content_type = "application/atom+xml"
    headers = {'content-type': content_type}

    s = requests.session()

    login = s.post(login_url, data=login_data)
    if login.status_code == 200:
        response = s.post(collections_url, data=atom, headers=headers)

        if response.status_code == 200:
            # update collection with date and syndicated url
            collection
        else:
            # record failure
            collection


def collection_as_atom(collection, encoding='utf-8'):
    """
    Serialise a collection to an Atom format

    Uses the profile from http://dataspace.metadata.net/doc/atom
    """
    output = StringIO.StringIO()
    site = Site.objects.get(id=1)

    link = get_site_url(site, collection.get_absolute_url())
    site_id = get_site_url(site, "/")

    handler = SimplerXMLGenerator(output, encoding)
    handler.startDocument()
    handler.startElement(u"entry", collection.entry_attributes())
    handler.addQuickElement(u"id", link)
    handler.addQuickElement(u"title", collection.title)
    handler.addQuickElement(u'content', collection.description, {'type': 'html'})
    if collection.date_published:
        handler.addQuickElement(u"published", rfc3339_date(collection.date_published).decode('utf-8'))
    if collection.last_published:
        handler.addQuickElement(u"updated", rfc3339_date(collection.last_published).decode('utf-8'))

    handler.addQuickElement(u"link", attrs={
            u'href':  'http://purl.org/dc/dcmitype/Collection',
            u'rel':   'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
            u'title': 'Collection'})

    handler.addQuickElement(u"rights", collection.rights)
    handler.startElement(u"rdfa:meta",
            {u'property': u'http://purl.org/dc/terms/accessRights',
                u'content': collection.access_rights})
    handler.endElement(u"rdfa:meta")

    handler.addQuickElement(u'link', attrs={
            u'rel': u'http://purl.org/dc/terms/publisher',
            u'href': settings.COLLECTION_CURATOR['href'],
            u'label': settings.COLLECTION_CURATOR['label']
        })

    handler.startElement(u"source", {})
    handler.addQuickElement(u"id", site_id)
    handler.addQuickElement(u"title", site.name)
    handler.startElement(u"author", {})
    handler.addQuickElement(u"name", collection.author.get_full_name())
    handler.addQuickElement(u"email", collection.author.email)
    handler.endElement(u"author")
    handler.endElement(u"source")

    handler.startElement(u"link",
            {u"rel": "http://xmlns.com/foaf/0.1/page",
             u"href": link})
    handler.endElement(u"link")

    handler.addQuickElement(u'category', attrs={
        u'term': u'http://purl.org/asc/1297.0/2008/for/1601',
        u'scheme': u'http://purl.org/asc/1297.0/2008/for/',
        u'label': u'1601 Anthropology'
        })

    add_categories(handler, collection, site)
    add_spatial(handler, collection, site)

    handler.endElement(u"entry")

    return output.getvalue()


def add_categories(handler, collection, site):
    for category in collection.get_categories():
# TODO: add this back when dataspace is fixed
#        cat_url = get_site_url(site, category.get_absolute_url())
        handler.addQuickElement(u'category', attrs={
#            u'term': cat_url,
            u'label': unicode(category)
        })


def add_spatial(handler, collection, site):
    for place in collection.get_places():
        place_url = get_site_url(site, place.get_absolute_url())
        handler.addQuickElement(u'link', attrs={
            u'rel': u'http://purl.org/dc/terms/spatial',
            u'href': place_url,
            u'title': unicode(place)
            })

        if place.latitude is not None:
            handler.addQuickElement(u'georss:point',
                unicode(place.latitude) + u" " + unicode(place.longitude)
            )

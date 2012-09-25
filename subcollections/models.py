from django.db import models
from datetime import datetime
from django.db.models.signals import post_save, post_delete
from cat.models import Category
from location.models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from django.utils.xmlutils import SimplerXMLGenerator
from django.core.urlresolvers import reverse
from utils.utils import get_site_url
import StringIO
from django.contrib.sites.models import Site
from django.utils.feedgenerator import rfc3339_date
import logging
import requests

logger = logging.getLogger(__name__)


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
            help_text="Date the collection was sent for syndication")
    syndication_result = models.TextField(blank=True, editable=False,
            help_text="Result from last syndication submission")

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

    def get_atom_url(self):
        return reverse('collection_atom_detail', args=[self.id])

    @staticmethod
    def entry_attributes():
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

        Returns a list of each place, ignoring places with blank names
        and ignoring places with duplicate names, even if they are different 'types'
        of place.

        Ordered from most all encompassing to most detailed.
        """
        items = self.items.all()
        names_set = set()
        places = []
        for place_type in (Locality, RegionDistrict, StateProvince, Country, GlobalRegion):
            for place in place_type.objects.filter(museumobject__in=items).distinct():
                if place.name and place.name not in names_set:
                    names_set.add(place.name)
                    places.append(place)
        places.reverse()
        return places

    def public_items(self):
        """
        Return a queryset of all public items
        """
        return self.items.filter(public=True)

    def as_atom(self, encoding='utf-8'):
        """
        Serialise to an Atom format

        Uses the profile from http://dataspace.metadata.net/doc/atom
        """
        syndication = Syndication.objects.get(id=1)
        output = StringIO.StringIO()
        site = Site.objects.get(id=1)

        link = get_site_url(site, self.get_absolute_url())
        site_id = get_site_url(site, "/")

        handler = SimplerXMLGenerator(output, encoding)
        handler.startDocument()
        handler.startElement(u"entry", self.entry_attributes())
        handler.addQuickElement(u"id", link)
        handler.addQuickElement(u"title", self.title)
        handler.addQuickElement(u'content', self.description, {'type': 'html'})
        if self.date_published:
            handler.addQuickElement(u"published", rfc3339_date(self.date_published).decode('utf-8'))
        if self.last_published:
            handler.addQuickElement(u"updated", rfc3339_date(self.last_published).decode('utf-8'))

        handler.addQuickElement(u"link", attrs={
                u'href':  'http://purl.org/dc/dcmitype/Collection',
                u'rel':   'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                u'title': 'Collection'})

        handler.addQuickElement(u"rights", self.rights)
        handler.startElement(u"rdfa:meta",
                {u'property': u'http://purl.org/dc/terms/accessRights',
                    u'content': self.access_rights})
        handler.endElement(u"rdfa:meta")

        handler.addQuickElement(u'link', attrs={
                u'rel': u'http://purl.org/dc/terms/publisher',
                u'href': syndication.curator_href,
                u'title': syndication.curator_name
            })

        handler.startElement(u"source", {})
        handler.addQuickElement(u"id", site_id)
        handler.addQuickElement(u"title", site.name)
        handler.startElement(u"author", {})
        handler.addQuickElement(u"name", self.author.get_full_name())
        handler.addQuickElement(u"email", self.author.email)
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

        # Published control
        draft = u'no' if self.is_public else u'yes'
        handler.startElement(u'app:control',
            {u'xmlns:app': u'http://www.w3.org/2007/app'})
        handler.addQuickElement(u'app:draft', draft)
        handler.endElement(u'app:control')

        self._add_categories(handler, site)
        self._add_spatial(handler, site)

        handler.endElement(u"entry")

        return output.getvalue()

    def _add_categories(self, handler, site):
        for category in self.get_categories():
    # TODO: add this back when dataspace is fixed
    #        cat_url = get_site_url(site, category.get_absolute_url())
            handler.addQuickElement(u'category', attrs={
    #            u'term': cat_url,
                u'term': unicode(category.name)
            })

    def _add_spatial(self, handler, site):
        for place in self.get_places():
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

    def update_after_syndication(self, response):
        """
        Update collection with date and syndication edit url
        """
        self.syndication_result = response.text
        self.last_syndicated = datetime.now()
        self.save()
        self.edit_url = self.find_edit_url(response.text)

    @staticmethod
    def find_edit_url(atom_string):
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(atom_string)
        alllinks = tree.findall('{http://www.w3.org/2005/Atom}link')
        return [c.get('href') for c in alllinks if c.get('rel') == 'edit'][0]
# The following is much nicer, but only works in python 2.7+ *sadface*
#        return tree.find('{http://www.w3.org/2005/Atom}link[@rel="edit"]').get('href')


class Syndication(models.Model):
    remote_url = models.CharField(max_length=300)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    curator_href = models.CharField(max_length=200, blank=True)
    curator_name = models.CharField(max_length=200, blank=True)

    # Constants
    content_type = "application/atom+xml"

    def __init__(self, *args, **kwargs):
        super(Syndication, self).__init__(*args, **kwargs)

        self.login_url = self.remote_url + "login"
        self.collections_url = self.remote_url + "collections"
        self.login_data = {'username': self.username,
                      'password': self.password}
        self.headers = {'content-type': self.content_type}

    def __unicode__(self):
        return self.remote_url

    def _login(self):
        """
        Login to syndication server
        """
        s = requests.session()
        self.session = s

        login = s.post(self.login_url, data=self.login_data)
        if login.status_code == 200:
            return True
        else:
            logger.error("Error logging in to syndication server %s",
                self.login_url)
            return False

    def syndicate_collection(self, collection):
        """
        Submit the collection to the syndication server
        """
        if self._login():
            if collection.edit_url == '':
                self._post_new(collection)
            else:
                self._update(collection)
        else:
            collection.syndication_result = 'Failed: unable to login to server'
            collection.save()

    def _post_new(self, collection):
        session = self.session
        response = session.post(self.collections_url,
            data=collection.as_atom(), headers=self.headers)

        if response.status_code == 201:
            collection.update_after_syndication(response)
        else:
            # record failure
            logger.error('Collection (id=%s) syndication POST (to %s) failed: %s',
                collection.id, self.collections_url, response.text)
            collection.syndication_result = response.text
        collection.save()

    def _update(self, collection):
        session = self.session
        response = session.put(collection.edit_url,
            data=collection.as_atom(), headers=self.headers)

        if response.status_code == 200:
            collection.update_after_syndication(response)
        else:
            # record failure
            logger.error('Collection (id=%s) syndication PUT (to %s) failed: %s',
                collection.id, collection.edit_url, response.text)
            collection.syndication_result = response.text
        collection.save()

    def delete_collection(self, collection):
        """
        Remove a collection from the syndication server
        """
        if collection.edit_url == '':
            logger.error('Unable to remove un-syndicated collection (id=%s)',
                collection.id)
            return

        if self._login():
            session = self.session
            response = session.delete(collection.edit_url)
            if response.status_code == 200:
                collection.edit_url = ''
                logger.info('Removed Collection (id=%s) from syndication server', collection.id)
            else:
                logger.error('Unable to remove collection (id=%s) from syndication server: %s %s',
                    response.status_code, response.text)
        else:
            logger.error('Unable to login to syndication server to remove collection (id=%s)',
                collection.id)


def queue_for_syndication(instance, **kwargs):
    collection = instance

    # Collection is updated with new dates and edit urls
    # we need to disconnect signal handler to prevent a loop
    post_save.disconnect(queue_for_syndication, sender=Collection)

    if collection.is_syndicated:
        syndication = Syndication.objects.get(id=1)
        try:
            syndication.syndicate_collection(collection)
        except:
            logger.exception("Error syndicating collection (id=%s)", collection.id)
    else:
        if collection.edit_url != '':
            syndication = Syndication.objects.get(id=1)
            syndication.delete_collection(collection)
            collection.save()

    post_save.connect(queue_for_syndication, sender=Collection)

post_save.connect(queue_for_syndication, sender=Collection)


def delete_from_syndication(instance, **kwargs):
    collection = instance
    if collection.is_syndicated:
        syndication = Syndication.objects.get(id=1)
        syndication.delete_collection(collection)


post_delete.connect(delete_from_syndication, sender=Collection)









from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, rfc3339_date
from subcollections.models import Collection
from django.shortcuts import get_object_or_404
from django.utils.xmlutils import SimplerXMLGenerator
from utils.utils import get_site_url
from django.http import HttpResponse
from django.contrib.sites.models import get_current_site


class AllCollectionsFeed(Feed):
    """
    Provides a feed for all collections in the system.
    """
    feed_type = Atom1Feed
    title = "Collection Feed"
    link = "/collections/"
    description = "Updates on UQAM collections"

    def items(self):
        return Collection.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description


class CollectionFeed(Feed):
    """
    Provides a feed for individual collections.

    Lists all of the artefacts in the collection.
    """
    feed_type = Atom1Feed
    description_template = 'feeds/collection_description.html'

    def get_object(self, request, collection_id):
        return get_object_or_404(Collection, pk=collection_id)

    def link(self, collection):
        return collection.get_absolute_url()

    def title(self, collection):
        return "UQAM Collection: %s" % collection.title

    def description(self, collection):
        return collection.description

    def items(self, collection):
        return collection.items.all()

    def item_description(self, item):
        return item.description


def write_collection_as_atom(request, collection, encoding='utf-8', mimetype='text/plain'):
    """
    Serialise a collection to an Atom format

    Uses the profile from http://dataspace.metadata.net/doc/atom
    """
    response = HttpResponse(mimetype=mimetype)
    current_site = get_current_site(request)

    link = get_site_url(request, collection.get_absolute_url())
    site_id = get_site_url(request, "/")

    handler = SimplerXMLGenerator(response, encoding)
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
            { u'property': u'http://purl.org/dc/terms/accessRights',
                u'content': collection.access_rights})
    handler.endElement(u"rdfa:meta")

    handler.startElement(u"author", {})
    handler.addQuickElement(u"name", collection.author.get_full_name())
    handler.addQuickElement(u"email", collection.author.email)
    handler.endElement(u"author")

    handler.startElement(u"source", {})
    handler.addQuickElement(u"id", site_id)
    handler.addQuickElement(u"title", current_site.name)
    handler.startElement(u"author", {})
    handler.addQuickElement(u"name", collection.author.get_full_name())
    handler.addQuickElement(u"email", collection.author.email)
    handler.endElement(u"author")
    handler.endElement(u"source")

    handler.startElement(u"link",
            {u"rel": "http://xmlns.com/foaf/0.1/page",
             u"href": link})
    handler.endElement(u"link")

    handler.endElement(u"entry")

    return response

from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from uqamcollections.models import Collection
from django.shortcuts import get_object_or_404

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

#def collection_feed(request, collection_id):
#    """
#    Create an Atom Feed for a collection
#    """
#    collection = get_object_or_404(Collection, pk=collection_id)




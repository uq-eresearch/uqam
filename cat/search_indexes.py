from haystack.indexes import SearchIndex, CharField
from haystack import site
from .models import MuseumObject


class MuseumObjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(MuseumObject, MuseumObjectIndex)

#class PersonIndex(SearchIndex):
#    text = CharField(document=True, use_template=True)
#
#site.register(Person, PersonIndex)

from haystack.indexes import SearchIndex, CharField, MultiValueField, BooleanField
from haystack import site
from .models import MuseumObject


class MuseumObjectImagesCharField(CharField):
    def prepare(self, obj):
        obj.public_images_count = obj.artefactrepresentation_set.count()
        return super(MuseumObjectImagesCharField, self).prepare(obj)


class MuseumObjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    categories = MultiValueField(faceted=True)
    item_name = CharField(model_attr='artefact_type', faceted=True)
    global_region = CharField(model_attr='global_region', faceted=True, default='')
    country = CharField(model_attr='country', faceted=True, default='')
    people = MultiValueField(faceted=True)
    has_images = BooleanField(faceted=True)
    list_row = MuseumObjectImagesCharField(use_template=True, template_name='snippets/item_list_row.html', indexed=False)
    grid_element = MuseumObjectImagesCharField(use_template=True, template_name='snippets/item_grid_element.html', indexed=False)

    def prepare_categories(self, object):
        return [unicode(cat.name) for cat in object.category.all()]

    def prepare_people(self, object):
        people = set()
        if object.maker:
            people.add(unicode(object.maker))
        people.add(unicode(object.donor))
        people.add(unicode(object.collector))
        return list(people)

    def prepare_has_images(self, object):
        return object.public_images().exists()

    def get_model(self):
        return MuseumObject

    def index_queryset(self):
        """
        Used when the entire index for model is updated.
        """
        ### TODO ###
        # Ignore private/reserved etc objects
        return self.get_model().objects.filter(public=True)

site.register(MuseumObject, MuseumObjectIndex)

from haystack import indexes
from .models import MuseumObject


class MuseumObjectImagesCharField(indexes.CharField):
    def prepare(self, obj):
        obj.public_images_count = obj.public_images().count()
        return super(MuseumObjectImagesCharField, self).prepare(obj)


class MuseumObjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    registration_number = indexes.IntegerField(model_attr='registration_number')
    categories = indexes.MultiValueField(faceted=True)
    item_name = indexes.CharField(model_attr='artefact_type', faceted=True)
    global_region = indexes.CharField(model_attr='global_region', faceted=True, default='')
    country = indexes.CharField(model_attr='country', faceted=True, default='')
    people = indexes.MultiValueField(faceted=True)
    has_images = indexes.BooleanField(faceted=True)
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

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.filter(public=True)


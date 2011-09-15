from django.db import models
from .thumbs import ImageWithThumbsField
from cat.models import MuseumObject
from south.modelsinspector import add_introspection_rules
import os.path
from filebrowser.fields import FileBrowseField

add_introspection_rules(
    [
        (
            (ImageWithThumbsField, ),
            [],
            {
                "verbose_name": ["verbose_name", {"default": None}],
                "name":         ["name",         {"default": None}],
                "width_field":  ["width_field",  {"default": None}],
                "height_field": ["height_field", {"default": None}],
                "sizes":        ["sizes",        {"default": None}],
            },
        ),
    ],
    ["^mediaman.thumbs.ImageWithThumbsField",])

class ArtefactRepresentation(models.Model):
    name = models.CharField(max_length=30, blank=True)
    image = ImageWithThumbsField(upload_to='mediareps/', sizes=((64,64),(400,350)))
    artefact = models.ForeignKey(MuseumObject)
    def __unicode__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=30, blank=True)
#    document = models.FileField(upload_to='docs/')
    document = FileBrowseField('Document', max_length=200, directory='docs/')
    def __unicode__(self):
        return self.name




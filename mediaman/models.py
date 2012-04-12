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
    ["^mediaman.thumbs.ImageWithThumbsField", ])

#from django.contrib.auth.models import User


class MediaFile(models.Model):
    md5sum = models.CharField(max_length=32, blank=True)
    filesize = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
#    uploaded_by = models.ForeignKey(User, related_name="+")
    mime_type = models.CharField(max_length=80)
    original_filename = models.CharField(max_length=30)
    name = models.CharField(max_length=30, blank=True)

    class Meta:
        abstract = True


class ArtefactRepresentation(MediaFile):
    image = ImageWithThumbsField(
                upload_to='mediareps/',
                sizes=((64, 64), (400, 350)))
    position = models.PositiveSmallIntegerField()
    artefact = models.ForeignKey(MuseumObject)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name


class ExternalArtefactRepresentation(models.Model):
    url = models.URLField()
    artefact = models.ForeignKey(MuseumObject)


class Document(MediaFile):
    document = models.FileField(upload_to='docs/')
#    document = FileBrowseField('Document', max_length=200, directory='docs/')

    def __unicode__(self):
        return self.name

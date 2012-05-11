from django.db import models
from mediaman.thumbs import ImageWithThumbsField
from cat.models import MuseumObject
from south.modelsinspector import add_introspection_rules
import os.path
from filebrowser.fields import FileBrowseField
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth.models import User

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


class MediaFile(models.Model):
    md5sum = models.CharField(max_length=32, blank=True)
    filesize = models.IntegerField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name="+",
            null=True, blank=True)
    mime_type = models.CharField(max_length=80, blank=True)
    original_filename = models.CharField(max_length=30)
    original_path = models.CharField(max_length=255, blank=True)
    original_filedate = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=30)

    class Meta:
        abstract = True

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
archival_storage = FileSystemStorage(location=settings.MEDIA_ROOT+'/archival')

class ArtefactRepresentation(MediaFile):
    image = ThumbnailerImageField(
        upload_to='mediareps/%Y/%m-%d/',
        storage=archival_storage,
        thumbnail_storage=default_storage)
#        resize_source=dict(
#            size=(64, 64), sharpen=True))
#    image = ImageWithThumbsField(
#                upload_to='mediareps/',
#                sizes=((64, 64), (400, 350)))
    position = models.PositiveSmallIntegerField()
    artefact = models.ForeignKey(MuseumObject)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name


def remove_delete_image_file(sender, instance, **kwargs):
    instance.image.delete(save=False)

from django.db.models.signals import post_delete
post_delete.connect(remove_delete_image_file)

#class ExternalArtefactRepresentation(models.Model):
#    url = models.URLField()
#    artefact = models.ForeignKey(MuseumObject)


class Document(MediaFile):
    document = models.FileField(upload_to='docs/')
#    document = FileBrowseField('Document', max_length=200, directory='docs/')

    def __unicode__(self):
        return self.name

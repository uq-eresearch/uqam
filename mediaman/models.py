from django.db import models
from mediaman.thumbs import ImageWithThumbsField
from cat.models import MuseumObject
from south.modelsinspector import add_introspection_rules
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.template import Template, Context

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
    md5sum = models.CharField(max_length=32, blank=True, editable=False)
    filesize = models.IntegerField(blank=True, null=True, editable=False)
    upload_date = models.DateTimeField(auto_now_add=True, editable=False)
    uploaded_by = models.ForeignKey(User, related_name="+",
            null=True, blank=True, editable=False)
    mime_type = models.CharField(max_length=150, blank=True, editable=False)
    original_filename = models.CharField(max_length=255, editable=False)
    original_path = models.CharField(max_length=255, blank=True, editable=False)
    original_filedate = models.DateTimeField(blank=True, null=True, editable=False)
    name = models.CharField(max_length=255, editable=False)

    def file_size(self):
        t = Template('{{ filesize|filesizeformat }}')
        c = Context({"filesize": self.filesize})
        return t.render(c)

    class Meta:
        abstract = True


archival_storage = FileSystemStorage(
        location=settings.MEDIA_ROOT + '/archival')


class ArtefactRepresentation(MediaFile):
    image = ThumbnailerImageField(
        upload_to='mediareps/%Y/%m-%d/',
        storage=archival_storage,
        thumbnail_storage=default_storage)
    position = models.PositiveSmallIntegerField()
    artefact = models.ForeignKey(MuseumObject)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name


def remove_delete_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

post_delete.connect(remove_delete_image_file, sender=ArtefactRepresentation)

#class ExternalArtefactRepresentation(models.Model):
#    url = models.URLField()
#    artefact = models.ForeignKey(MuseumObject)


class Document(MediaFile):
    document = models.FileField(upload_to='docs/%Y/%m-%d/')
    document_text = models.TextField(blank=True)
    public = models.BooleanField()

    def __unicode__(self):
        return self.name


def delete_document_file(sender, instance, **kwargs):
    if instance.document:
        instance.document.delete(save=False)
post_delete.connect(delete_document_file, sender=Document)

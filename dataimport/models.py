from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class ImportIssue(models.Model):
    """
    Tracks any problems which occurred when importing data.
    """
    description = models.CharField(max_length=200)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    has_been_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['description']

    def __unicode__(self):
        return self.description


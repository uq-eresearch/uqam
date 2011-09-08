from django.db import models
from .thumbs import ImageWithThumbsField
from cat.models import MuseumObject

# Create your models here.

class ArtefactRepresentation(models.Model):
    name = models.CharField(max_length=30)
    image = ImageWithThumbsField(upload_to='mediareps/', sizes=((64,64),(400,400)))
    artefact = models.ForeignKey(MuseumObject)

from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    agent = models.ForeignKey('cat.Person')
    items = models.ManyToManyField('cat.MuseumObject', related_name='items')



class Exhibition(Collection):
    start_date = models.DateField()
    end_date = models.DateField()

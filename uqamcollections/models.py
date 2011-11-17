from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    agent = models.ForeignKey('cat.Person')
    items = models.ManyToManyField('cat.MuseumObject', related_name='items', blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('collection_detail', [str(self.id)])



class Exhibition(Collection):
    start_date = models.DateField()
    end_date = models.DateField()

class Syndication(models.Model):
   remote_url = models.CharField(max_length=300) 

from django.db import models

# Create your models here.

class MuseumObject(models.Model):
    registration_number = models.IntegerField()
    old_registration_number = models.CharField(max_length=30, blank=True)
    functional_category = models.ForeignKey('FunctionalCategory')
    artefact_type = models.ForeignKey('ArtefactType', blank=True)
#    storage_location = models.CharField(max_length=30)
    acquisition_date = models.DateField(blank=True, null=True)
    acquisition_method = models.CharField(max_length=30)
    access_status = models.CharField(max_length=30, blank=True)
    loan_status = models.CharField(max_length=30)
    cultural_bloc = models.ForeignKey('CulturalBloc', null=True)
    country = models.CharField(max_length=30)
#    region = models.CharField(max_length=30)
#    place = models.CharField(max_length=30)
#    australian_state = models.CharField(max_length=30)
    place = models.ForeignKey('Place', null=True)
    collector = models.ForeignKey('Person', null=True)
#    how_collector_obtained = models.CharField(max_length=30)
#    photographer = models.CharField(max_length=30)
#    source = models.CharField(max_length=30)
#    how_source_obtained = models.CharField(max_length=30)
    maker_or_artist = models.CharField(max_length=30)
    site_name_number = models.CharField(max_length=30)
    raw_material = models.CharField(max_length=30)
    indigenous_name = models.CharField(max_length=50)
    recorded_use = models.CharField(max_length=30)
    assoc_cultural_group = models.CharField(max_length=50)
#    exhibition_history = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
#    condition_details = models.CharField(max_length=30)
    width = models.IntegerField(null=True,blank=True)
    length = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    depth = models.IntegerField(null=True,blank=True)
    circumference = models.IntegerField(null=True,blank=True)
    longitude = models.IntegerField(null=True,blank=True)
    latitude = models.IntegerField(null=True,blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('artefact_view', [str(self.id)])

    class Meta:
        ordering = ['registration_number']

    def __unicode__(self):
        return "MO: %d" % self.registration_number
    


class FunctionalCategory(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Functional categories"

class CulturalBloc(models.Model):
    name = models.CharField(max_length=30)
    @models.permalink
    def get_absolute_url(self):
        return ('culturalbloc_detail', [str(self.name)])
    def __unicode__(self):
        return self.name

class ArtefactType(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Place(models.Model):
    country = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=40, blank=True)
    australian_state = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=30)
    comments = models.TextField(blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "People"

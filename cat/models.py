from django.db import models

# Create your models here.


class MuseumObject(models.Model):
    registration_number = models.CharField(max_length=30)
    old_registration_number = models.CharField(max_length=30)
    functional_category = models.ForeignKey('FunctionalCategory')
#    artefact_type = models.CharField(max_length=30)
#    storage_location = models.CharField(max_length=30)
#    acquisition_date = models.DateField()
#    acquisition_method = models.CharField(max_length=30)
#    access_status = models.CharField(max_length=30)
#    loan_status = models.CharField(max_length=30)
#    cultural_block = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
#    region = models.CharField(max_length=30)
#    place = models.CharField(max_length=30)
#    australian_state = models.CharField(max_length=30)
#    collector = models.CharField(max_length=30)
#    how_collector_obtained = models.CharField(max_length=30)
#    photographer = models.CharField(max_length=30)
#    source = models.CharField(max_length=30)
#    how_source_obtained = models.CharField(max_length=30)
#    maker_or_artist = models.CharField(max_length=30)
#    site_name_number = models.CharField(max_length=30)
#    raw_material = models.CharField(max_length=30)
#    indigenous_name = models.CharField(max_length=30)
#    recorded_use = models.CharField(max_length=30)
#    exhibition_history = models.CharField(max_length=30)
    description = models.TextField()
    comment = models.TextField()
#    condition_details = models.CharField(max_length=30)
    
    class Meta:
        ordering = ['registration_number']

    def __unicode__(self):
        return "MO: " + self.registration_number
    


class FunctionalCategory(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Functional categories"


class Person(models.Model):
    name = models.CharField(max_length=30)

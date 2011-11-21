from django.db import models

# Create your models here.

class MuseumObject(models.Model):
    id = models.IntegerField(primary_key=True)
    registration_number = models.IntegerField(db_index=True, unique=True)
    old_registration_number = models.CharField(max_length=10, blank=True)
    other_number = models.CharField(max_length=10, blank=True)
    reg_counter = models.CharField(max_length=10, blank=True)
    functional_category = models.ForeignKey('FunctionalCategory')
    artefact_type = models.ForeignKey('ArtefactType', blank=True)
    storage_section = models.CharField(max_length=4, blank=True)
    storage_unit = models.CharField(max_length=4, blank=True)
    storage_bay = models.CharField(max_length=4, blank=True)
    storage_shelf_box_drawer = models.CharField(max_length=4, blank=True)
    acquisition_date = models.CharField(max_length=30, blank=True)
    acquisition_method = models.CharField(max_length=30, blank=True)
    loan_status = models.CharField(max_length=30, blank=True)
    access_status = models.CharField(max_length=30, blank=True)
    cultural_bloc = models.ForeignKey('CulturalBloc', null=True)
    place = models.ForeignKey('Place', null=True)
    donor = models.ForeignKey('Person', null=True, blank=True, related_name="donated_objects")
    donor_2 = models.ForeignKey('Person', null=True, blank=True, related_name="donated_objects_2")
    how_donor_obtained = models.CharField(max_length=50, blank=True)
    ## TODO: when_donor_obtained should be DateField
    when_donor_obtained = models.CharField(max_length=50, blank=True)

    photographer = models.CharField(max_length=30)
    collector = models.ForeignKey('Person', null=True, blank=True, related_name="collected_objects")
    collector_2 = models.ForeignKey('Person', null=True, blank=True, related_name="collected_objects_2")
    how_collector_obtained = models.CharField(max_length=30, blank=True)
    when_collector_obtained = models.CharField(max_length=30, blank=True)

    source = models.CharField(max_length=30)
    how_source_obtained = models.CharField(max_length=30)

    maker_or_artist = models.CharField(max_length=30, blank=True)
    site_name_number = models.CharField(max_length=30, blank=True)
    raw_material = models.CharField(max_length=30, blank=True)
    indigenous_name = models.CharField(max_length=50, blank=True)
    recorded_use = models.CharField(max_length=30, blank=True)
    assoc_cultural_group = models.CharField(max_length=50, blank=True)
#    exhibition_history = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
#    condition_details = models.CharField(max_length=30)
    width = models.IntegerField(null=True,blank=True)
    length = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    depth = models.IntegerField(null=True,blank=True)
    circumference = models.IntegerField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    
    related_documents = models.ManyToManyField('mediaman.Document', related_name='related_museumobjects', null=True, blank=True)
    @models.permalink
    def get_absolute_url(self):
        return ('artefact_view', [str(self.id)])

    class Meta:
        ordering = ['registration_number']

    def __unicode__(self):
        return "%s: %d" % (self.artefact_type, self.registration_number)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__startswith",)

    


class FunctionalCategory(models.Model):
    name = models.CharField('function category', max_length=30)
    definition = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Functional categories"
        ordering = ['name']

class CulturalBloc(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    definition = models.TextField(blank=True)
    @models.permalink
    def get_absolute_url(self):
        return ('culturalbloc_detail', [str(self.name)])
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class ArtefactType(models.Model):
    name = models.CharField(max_length=30)
    definition = models.TextField(blank=True)
    see_also = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Place(models.Model):
    country = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=40, blank=True)
    australian_state = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return ' > '.join([self.country, self.region, self.name])
    @models.permalink
    def get_absolute_url(self):
        return ('place_detail', [str(self.id)])
    def geocode(self):
        from geopy import geocoders
        geonames = geocoders.GeoNames()
        place, (lat, lng) = geonames.geocode('%s, %s' % (self.name, self.country,),
                                             exactly_one=False)[0]
        self.latitude = lat
        self.longitude = lng
        self.save()


class Person(models.Model):
    name = models.CharField(max_length=30)
    comments = models.TextField(blank=True)
    related_documents = models.ManyToManyField('mediaman.Document', related_name='related_people',blank=True)
    @models.permalink
    def get_absolute_url(self):
        return ('person_detail', [str(self.id)])
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "People"
    @staticmethod
    def autocomplete_search_fields():
        return ("name__iexact",)

class Region(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    """
    A hierarchical set of categories for classifying Museum Objects
    """
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")
    def __unicode__(self):
        if self.parent:
            return self.parent.__unicode__() + " :: " + self.name
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

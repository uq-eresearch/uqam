from django.db import models
import string


class MuseumObject(models.Model):
    """
    An object held by the museum, typically a physical object or photo
    """
    id = models.IntegerField(primary_key=True)
    registration_number = models.IntegerField(db_index=True, unique=True)
    old_registration_number = models.CharField(max_length=50, blank=True)
    other_number = models.CharField(max_length=50, blank=True)
    reg_counter = models.CharField(max_length=50, blank=True)

    functional_category = models.ForeignKey('FunctionalCategory')
    artefact_type = models.ForeignKey('ArtefactType', blank=True)
    category = models.ManyToManyField('Category', blank=True)

    storage_section = models.CharField(max_length=4, blank=True)
    storage_unit = models.CharField(max_length=4, blank=True)
    storage_bay = models.CharField(max_length=4, blank=True)
    storage_shelf_box_drawer = models.CharField(max_length=4, blank=True)

    acquisition_date = models.CharField(max_length=50, blank=True)
    acquisition_method = models.CharField(max_length=50, blank=True)
    loan_status = models.CharField(max_length=50, blank=True)
    access_status = models.CharField(max_length=50, blank=True)
    reg_info = models.TextField("registration information", blank=True)

    cultural_bloc = models.ForeignKey('CulturalBloc', null=True)
    place = models.ForeignKey('Place', null=True, db_index=True)

    donor = models.ForeignKey(
            'Person', 
            null=True, 
            blank=True, 
            db_index=True,
            related_name="donated_objects")
    donor_2 = models.ForeignKey(
            'Person', 
            null=True, 
            blank=True, 
            related_name="donated_objects_2")
    how_donor_obtained = models.CharField(max_length=50, blank=True)
    ## TODO: when_donor_obtained should be DateField
    when_donor_obtained = models.CharField(max_length=50, blank=True)

    photographer = models.CharField(max_length=100)
    collector = models.ForeignKey(
            'Person', 
            null=True, 
            blank=True, 
            db_index=True,
            related_name="collected_objects")
    collector_2 = models.ForeignKey(
            'Person', 
            null=True, 
            blank=True, 
            related_name="collected_objects_2")
    how_collector_obtained = models.CharField(max_length=50, blank=True)
    when_collector_obtained = models.CharField(max_length=50, blank=True)

    source = models.CharField(max_length=50)
    how_source_obtained = models.CharField(max_length=50)

    maker = models.ForeignKey('Maker', null=True, blank=True)
    manufacture_technique = models.CharField(max_length=200, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    site_name_number = models.CharField(max_length=150, blank=True)
    raw_material = models.CharField(max_length=150, blank=True)
    indigenous_name = models.CharField(max_length=100, blank=True)
    recorded_use = models.CharField(max_length=300, blank=True)
    assoc_cultural_group = models.CharField(max_length=100, blank=True)
    exhibition_history = models.TextField(blank=True)
    description = models.TextField(blank=True)

    is_public_comment = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    private_comment = models.TextField(
            blank=True, 
            help_text="Only visible to staff")
    significance = models.TextField("statement of significance",
            blank=True)

    width = models.IntegerField(null=True,blank=True)
    length = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    depth = models.IntegerField(null=True,blank=True)
    circumference = models.IntegerField(null=True,blank=True)

    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    
    related_documents = models.ManyToManyField(
            'mediaman.Document', 
            related_name='related_museumobjects', 
            null=True, blank=True)

    def dimensions(self):
        '''Returns textual dimensions for the item
        
        Combining length, width, height, depth, circumference
        '''
        dims = [self.length, self.width, self.height, self.depth, self.circumference]
        dims = [str(d/10) for d in dims if d != None]
        s = string.join(dims, " x ")
        return s + " cm" if s else ''


    @models.permalink
    def get_absolute_url(self):
        return ('artefact_view', [str(self.id)])

    class Meta:
        ordering = ['registration_number']

    def __unicode__(self):
        return "%s: %d" % (self.artefact_type, self.registration_number)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact",)

    


class FunctionalCategory(models.Model):
    name = models.CharField('function category', max_length=30, unique=True)
    definition = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Functional categories"
        ordering = ['name']

class CulturalBloc(models.Model):
    name = models.CharField(max_length=30, db_index=True, unique=True)
    definition = models.TextField(blank=True)
    @models.permalink
    def get_absolute_url(self):
        return ('culturalbloc_detail', [str(self.name)])
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class ArtefactType(models.Model):
    """
    The type or intended use of an object

    Soon to be superseded by `Category`
    """
    name = models.CharField(max_length=150, unique=True)
    definition = models.TextField(blank=True)
    see_also = models.CharField(max_length=150, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Place(models.Model):
    country = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=40, blank=True)
    australian_state = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=150)

    is_corrected = models.BooleanField(default=False, 
            help_text="Has someone manually moved the marker to it's correct location.")
    gn_name = models.CharField(max_length=100, help_text="GeoNames Name", blank=True)
    gn_id = models.CharField(max_length=20, help_text="GeoNames ID", blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    class Meta:
        ordering = ["id"]
    def __unicode__(self):
        return ' > '.join([self.country, self.region, self.name])
    @models.permalink
    def get_absolute_url(self):
        return ('place_detail', [str(self.id)])
    def get_geonames_url(self):
        if self.gn_id:
            return "http://www.geonames.org/%s" % self.gn_id
        else:
            return False
    def get_kml_coordinates(self):
        return "%s,%s,0" % (self.longitude, self.latitude)
    def geocode(self, force=False):
        """
        Lookup the latitude and longitude of this place with GeoNames

        Place must be saved after use. Set `force` to re-lookup the location.
        
        Can take a few seconds to return, since this uses a network request.
        """
        if self.gn_id and not force:
            return
        from utils import geocoders
        geonames = geocoders.GeoNamesWithId()
        place, geonameId, (lat, lng) = geonames.geocode('%s, %s' %
                                                (self.name, self.country,),
                                                exactly_one=False)[0]
        self.gn_name = place
        self.gn_id = geonameId
        self.latitude = lat
        self.longitude = lng


class Person(models.Model):
    """
    A collector or photographer who has contributed to the museum
    """
    name = models.CharField(max_length=150)
    comments = models.TextField(blank=True)
    related_documents = models.ManyToManyField('mediaman.Document',
            related_name='related_people',blank=True)

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
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    """
    A hierarchical set of categories for classifying Museum Objects
    """
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', blank=True,
            null=True, related_name="children")
    slug = models.SlugField(help_text="Used in URLs")

    def __unicode__(self):
        if self.parent:
            return self.parent.__unicode__() + " :: " + self.name
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"
        unique_together = (("slug", "parent"), ("name", "parent"))
    def get_absolute_url(self):
        url = "/%s/" % self.slug
        category = self
        while category.parent:
            url = "/%s%s" % (category.parent.slug, url)
            category = category.parent
        url = "/categories" + url
        return url



class Maker(models.Model):
    """A person or entity who created an item in the collection"""
    name = models.CharField(max_length=200, unique=True)
    comment = models.TextField(blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('maker_detail', [str(self.id)])

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

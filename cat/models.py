from django.db import models
import string


class AcquisitionMethod(models.Model):
    method = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.method


class LoanStatus(models.Model):
    status = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.status


class AccessStatus(models.Model):
    status = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.status


class Obtained(models.Model):
    how = models.CharField(max_length=50, unique=True)
    definition = models.CharField(max_length=150)

    def __unicode__(self):
        return self.how


class MuseumObject(models.Model):
    """
    An object held by the museum, typically a physical object or photo
    """
    id = models.IntegerField(primary_key=True)
    registration_number = models.IntegerField(db_index=True, unique=True)
    old_registration_number = models.CharField(max_length=50, blank=True)
    other_number = models.CharField(max_length=50, blank=True)
    reg_counter = models.CharField(max_length=50, blank=True)

    functional_category = models.ForeignKey('FunctionalCategory',
            verbose_name='previous category name',
            help_text='Functional Category from the old database')
    artefact_type = models.ForeignKey('ArtefactType')
    category = models.ManyToManyField('Category', blank=True,
            help_text='New style categories')

    storage_section = models.CharField(max_length=4, blank=True)
    storage_unit = models.CharField(max_length=4, blank=True)
    storage_bay = models.CharField(max_length=4, blank=True)
    storage_shelf_box_drawer = models.CharField(max_length=4, blank=True)

    acquisition_date = models.DateField("Date acquired by museum",
            null=True, blank=True)
    acquisition_method = models.ForeignKey(AcquisitionMethod, null=True)
    loan_status = models.ForeignKey(LoanStatus, null=True,
            help_text='Is object on outwards/inwards loan')
    access_status = models.ForeignKey(AccessStatus, null=True)
    reg_info = models.TextField("registration information", blank=True)

    registered_by = models.ForeignKey('parties.MuseumStaff', null=True)
    registration_date = models.DateField(null=True)

    cultural_bloc = models.ForeignKey('CulturalBloc', null=True,
            help_text='Old region classification')
    place = models.ForeignKey('location.Place', null=True, db_index=True,
            help_text='Where the object is from')

    donor = models.ForeignKey(
            'parties.Person',
            null=True,
            blank=True,
            db_index=True,
            related_name="donated_objects",
            help_text='Main donor record')
    donor_2 = models.ForeignKey(
            'parties.Person',
            null=True,
            blank=True,
            related_name="donated_objects_2",
            help_text='2nd Imported donor record, possibly historic')
    how_donor_obtained = models.ForeignKey(Obtained, null=True,
            related_name='donor_obtained')
    ## TODO: when_donor_obtained should be DateField
    ### But contains some imprecise dates
    when_donor_obtained = models.CharField(max_length=50, blank=True)

    photographer = models.CharField(max_length=100)
    collector = models.ForeignKey(
            'parties.Person',
            null=True,
            blank=True,
            db_index=True,
            related_name="collected_objects")
    collector_2 = models.ForeignKey(
            'parties.Person',
            null=True,
            blank=True,
            related_name="collected_objects_2")
    how_collector_obtained = models.ForeignKey(Obtained, null=True,
            related_name="collector_obtained")
    when_collector_obtained = models.CharField(max_length=50, blank=True,
            help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

    source = models.CharField(max_length=50)
    how_source_obtained = models.ForeignKey(Obtained, null=True,
            related_name='source_obtained')

    maker = models.ForeignKey('parties.Maker', null=True, blank=True)
    manufacture_technique = models.CharField(max_length=200, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    site_name_number = models.CharField(max_length=150, blank=True)
    raw_material = models.CharField(max_length=150, blank=True)
    indigenous_name = models.CharField(max_length=100, blank=True)
    recorded_use = models.CharField(max_length=300, blank=True)
    assoc_cultural_group = models.CharField(max_length=100, blank=True)
    exhibition_history = models.TextField(blank=True)

    category_illustrated = models.CharField(max_length=100, blank=True)
    artefact_illustrated = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    is_public_comment = models.BooleanField(default=False,
            help_text='Is comment allowed to be shown publicly')
    comment = models.TextField(blank=True)
    private_comment = models.TextField(
            blank=True,
            help_text="Only visible to staff")
    significance = models.TextField("statement of significance",
            blank=True)

    width = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    circumference = models.IntegerField(null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    related_documents = models.ManyToManyField(
            'mediaman.Document',
            related_name='related_museumobjects',
            null=True, blank=True)

    def dimensions(self):
        '''Returns textual dimensions for the item

        Combining length, width, height, depth, circumference
        '''
        dims = [self.length, self.width, self.height,
                self.depth, self.circumference]
        dims = [str(d / 10) for d in dims if d != None]
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
    """
    name = models.CharField(max_length=150, unique=True)
    definition = models.TextField(blank=True)
    see_also = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    """
    A hierarchical set of categories for classifying Museum Objects
    """
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', blank=True,
            null=True, related_name="children")
    slug = models.SlugField(help_text="Used in URLs")
    suggested_artefact_types = models.ManyToManyField(ArtefactType,
            related_name='categories', null=True)

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


class Reference(models.Model):
    """
    Publications mentioning a museum object
    """
    museum_object = models.ForeignKey(MuseumObject)
    author = models.CharField(max_length=150)
    publications_details = models.CharField(max_length=500)

    def __unicode__(self):
        return self.museum_object.__unicode__() + self.publications_details


class PhotoRecord(models.Model):
    """
    Photographic record of a museum object
    """
    museum_object = models.ForeignKey(MuseumObject)
    phototype = models.ForeignKey('PhotoType')
    comments = models.CharField(max_length=200)


class PhotoType(models.Model):
    """
    Type of photographic record
    """
    phototype = models.CharField(max_length=50, unique=True)
    definition = models.CharField(max_length=100)

    def __unicode__(self):
        return self.phototype

from django.db import models


class Person(models.Model):
    """
    A collector or photographer who has contributed to the museum
    """
    name = models.CharField(help_text="Used internally and for sorting",
        unique=True, max_length=150)
    display_name = models.CharField(help_text="For display purposes",
        max_length=150)
    comments = models.TextField(blank=True)
    related_documents = models.ManyToManyField('mediaman.Document',
            related_name='related_people', blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('person_detail', [str(self.id)])

    def __unicode__(self):
        return self.display_name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "People"

    @staticmethod
    def autocomplete_search_fields():
        return ("name__iexact",)


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

    @staticmethod
    def autocomplete_search_fields():
        return ("name__iexact",)


class Client(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.CharField(blank=True, max_length=80)
    position = models.CharField(blank=True, max_length=80)
    address = models.TextField(blank=True)
    town_suburb = models.CharField(blank=True, max_length=80)
    state = models.CharField(blank=True, max_length=30)
    postcode = models.CharField(blank=True, max_length=10)
    country = models.CharField(blank=True, max_length=50)

    phone1 = models.CharField(blank=True, max_length=20)
    phone2 = models.CharField(blank=True, max_length=20)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__iexact",)


class MuseumStaff(models.Model):
    name = models.CharField(max_length=200, unique=True)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Museum staff"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__iexact",)

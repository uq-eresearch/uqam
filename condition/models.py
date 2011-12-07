from django.db import models

from cat.models import MuseumObject
from loans.models import MuseumStaff


class Conservator(models.Model):
    title = models.CharField(max_length=30, blank=True)
    firstname = models.CharField(max_length=60, blank=True)
    surname = models.CharField(max_length=60, blank=True)
    organisation = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=60, blank=True)
    fax = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.title, self.firstname, self.surname)
    class Meta:
        ordering = ['surname', 'firstname']


class ConditionReport(models.Model):
    item = models.ForeignKey(MuseumObject)
    condition = models.CharField(max_length=30)
    date = models.DateField()
    details = models.TextField()
    report_author = models.ForeignKey(MuseumStaff, null=True,blank=True)
    change_reason = models.TextField()
    def __unicode__(self):
        return "Condition Report: %s %s" % (self.item, self.date)
    class Meta:
        ordering = ['item']

class ConservationAction(models.Model):
    item = models.ForeignKey(MuseumObject)
    date = models.DateField()
    action = models.CharField(max_length=60)
    details = models.TextField()
    future_conservation = models.TextField(blank=True)
    future_conservation_date = models.DateField(null=True,blank=True)
    comments = models.TextField(blank=True)
    material_used = models.TextField(blank=True)
    conservator = models.ForeignKey(Conservator,null=True)
    def __unicode__(self):
        return "%s: %s" % (self.item, self.action)
    class Meta:
        ordering = ['item']

class Deaccession(models.Model):
    item = models.ForeignKey(MuseumObject)
    reason = models.TextField()
    date = models.DateField(blank=True, null=True)
    person = models.ForeignKey(MuseumStaff)
    def __unicode__(self):
        return "Deaccession: %s" % self.item
    class Meta:
        ordering = ['item']

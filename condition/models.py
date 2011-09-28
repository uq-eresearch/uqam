from django.db import models

from cat.models import MuseumObject, Person

# Create your models here.

class ConditionReport(models.Model):
    item = models.ForeignKey(MuseumObject)
    condition = models.CharField(max_length=30)
    date = models.DateField()
    details = models.TextField()
    report_author = models.ForeignKey(Person)
    change_reason = models.CharField(max_length=50)

class ConservationAction(models.Model):
    item = models.ForeignKey(MuseumObject)
    date = models.DateField()
    action = models.CharField(max_length=30)
    details = models.TextField()
    future_conservation = models.TextField()
    future_conservation_date = models.DateField()
    comments = models.TextField()
    material_used = models.CharField(max_length=100)
    conservator = models.ForeignKey(Person)

class Deaccession(models.Model):
    item = models.ForeignKey(MuseumObject)
    reason = models.TextField()
    date = models.DateField(blank=True, null=True)
    person = models.ForeignKey(Person)

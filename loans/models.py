from django.db import models
from cat.models import MuseumObject

RETURNED_OPTIONS = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Extended', 'Extended')
    ]

LOAN_TYPES = [
    ('Internal', 'Internal'),
    ('External', 'External')
    ]


class LoanAgreement(models.Model):
    ref = models.CharField(max_length=10)
    client = models.ForeignKey('Client')
    date_borrowed = models.DateField()
    return_date = models.DateField()
    approved_by = models.ForeignKey('MuseumStaff',
            related_name="approved_by")
    prepared_by = models.ForeignKey('MuseumStaff',
            related_name="prepared_by")
    loan_type = models.CharField(blank=True, max_length=20,
            choices=LOAN_TYPES)
    special_loan_conditions = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=200)
    purpose = models.ForeignKey('LoanPurpose', null=True)
    returned = models.CharField(blank=True, max_length=100,
            choices=RETURNED_OPTIONS)
    comments = models.TextField(blank=True)
    items = models.ManyToManyField(MuseumObject, through='LoanItem')

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return "LoanAgreement " + str(self.id) + " " + self.ref


class LoanPurpose(models.Model):
    purpose = models.CharField(max_length=20)

    def __unicode__(self):
        return self.purpose


class LoanItem(models.Model):
    loan = models.ForeignKey(LoanAgreement)
    item = models.ForeignKey(MuseumObject)
    out_condition = models.CharField(blank=True, max_length=30)
    return_condition = models.CharField(blank=True, max_length=30)

    class Meta:
        unique_together = ('loan', 'item')

    def __unicode__(self):
        return self.item.__unicode__()


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


class MuseumStaff(models.Model):
    name = models.CharField(max_length=200)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Museum staff"
        ordering = ['name']

    def __unicode__(self):
        return self.name

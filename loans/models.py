from django.db import models
from cat.models import MuseumObject


class LoanAgreement(models.Model):
    ref = models.CharField(max_length=10)
    client = models.ForeignKey('Client')
    date_borrowed = models.DateField()
    return_date = models.DateField()
    approved_by = models.ForeignKey('MuseumStaff', related_name="approved_by")
    prepared_by = models.ForeignKey('MuseumStaff', related_name="prepared_by")
    loan_type = models.CharField(max_length=20)
    loan_purpose = models.CharField(max_length=20)
    special_loan_conditions = models.TextField()
    comments = models.TextField()
    items = models.ManyToManyField(MuseumObject, through='LoanItem')

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return "LoanAgreement " + str(self.id) + " " + self.ref

class LoanItem(models.Model):
    loan = models.ForeignKey(LoanAgreement)
    item = models.ForeignKey(MuseumObject)
    out_condition = models.CharField(max_length=30)
    return_condition = models.CharField(max_length=30)

    def __unicode__(self):
        return self.item.__unicode__()


class Client(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.CharField(max_length=80)
    address = models.CharField(max_length=300)
    town_suburb = models.CharField(max_length=80)
    state = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)

    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class MuseumStaff(models.Model):
    name = models.CharField(max_length=200)
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

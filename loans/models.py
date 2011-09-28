from django.db import models

from cat.models import MuseumObject, Person

# Create your models here.

class LoanAgreement(models.Model):
    ref = models.CharField(max_length=10)
    client = models.ForeignKey('Client')
    date_borrowed = models.DateField()
    return_date = models.DateField()
    approved_by = models.ForeignKey(Person)
    prepared_by = models.ForeignKey(Person)
    loan_type = models.CharField(max_length=20)
    loan_purpose = models.CharField(max_length=20)
    special_loan_conditions = models.TextField()
    comments = models.TextField()
    loan_items = models.OneToManyField(MuseumObject)
    out_condition = models.CharField(max_length=30)
    return_condition = models.CharField(max_length=30)


class Client(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.CharField(max_length=80)
    address = models.CharField(max_length=300)
    town_suburb = models.CharField(max_length=80)
    state = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)

    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20)

from django.core.management.base import BaseCommand, CommandError
from cat.models import MuseumObject, FunctionalCategory, ArtefactType, CulturalBloc
from cat.models import Person, Place
from django.core import management
from django.db import transaction

import csv
import sys
import os
import string

ARTEFACT_CSV = 'Artefact.csv'

def prepare_stdout():
    unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbuffered

def clean_row(row):
    for key,value in row.items():
        row[key] = value.strip()
    row["Functional_Category"] = string.capwords(row["Functional_Category"])
    row["Loan_Status"] = string.capwords(row["Loan_Status"])
    return row


@transaction.commit_manually
def import_people(path):
    data = csv.DictReader(open(path + "Person.csv"))

    for r in data:
        for key,value in r.items():
            r[key] = value.strip()
        p = Person()
        p.id = r["Person idnmbr"]
        p.name = r["Name"]
        p.comments = r["PersonComments"]
        p.save()
    transaction.commit()




@transaction.commit_manually
def import_artefacts(path):
    data = csv.DictReader(open(path + ARTEFACT_CSV))

    count = 0
    prepare_stdout()


    for r in data:
        sys.stdout.write('.')
        r = clean_row(r)

        m = MuseumObject()

        # Map simple fields
        m.registration_number = r["Reg_counter"]
        m.old_registration_number = r["Old_Registration_nmbr"]
        if r["Aquisition_Date"] != "":
            m.acquisition_date = r["Aquisition_Date"]
        m.acquisition_method = r["Aquisition_Method"]
        m.access_status = r["AccessStatus"]
        m.loan_status = r["Loan_Status"]
        m.country = r["Country_Name"]
        m.description = r["Description"]
        m.comment = r["Comment"]

        # Map relations
        fc, created = FunctionalCategory.objects.get_or_create(name=r['Functional_Category'])
        m.functional_category = fc

        pl, created = Place.objects.get_or_create(name=r['Place'],
                                                  australian_state=r['State_Abbr'],
                                                  region=r['Region'],
                                                  country=r['Country_Name'])
        m.place = pl

        at, created = ArtefactType.objects.get_or_create(name=r['Artefact_TypeName'])
        m.artefact_type = at

        cb, created = CulturalBloc.objects.get_or_create(name=r['CulturalBloc'])
        m.cultural_bloc = cb

        p = Person.objects.get(pk=int(r["Collector_photographerID"]))
        m.collector = p

        m.save()

        count += 1
        if count % 1000:
            sys.stdout.write('C')
            transaction.commit()
            break


class Command(BaseCommand):

    help = "Import an Anthropology Museum catalogue"

    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("need exactly one argument for db directory")

        dir, = args

        management.call_command('reset', 'cat', interactive=False)
        management.call_command('syncdb', interactive=False)

        import_people(dir)
        import_artefacts(dir)

        

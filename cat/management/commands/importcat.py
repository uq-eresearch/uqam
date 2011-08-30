from django.core.management.base import BaseCommand, CommandError
from cat.models import MuseumObject, FunctionalCategory, ArtefactType, CulturalBloc
from django.core import management
from django.db import transaction

import csv
import sys
import os

ARTEFACT_CSV = 'Artefact.csv'

def prepare_stdout():
    unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbuffered

@transaction.commit_manually
def import_csv(path):
    data = csv.DictReader(open(path + ARTEFACT_CSV))

    count = 0
    prepare_stdout()


    for r in data:
        sys.stdout.write('.')

        for key,value in r.items():
            r[key] = value.strip()

        m = MuseumObject()
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

        fc, created = FunctionalCategory.objects.get_or_create(name=r['Functional_Category'])
        m.functional_category = fc

        at, created = ArtefactType.objects.get_or_create(name=r['Artefact_TypeName'])
        m.artefact_type = at

        cb, created = CulturalBloc.objects.get_or_create(name=r['CulturalBloc'])
        m.cultural_bloc = cb

        m.save()

        count += 1
        if count > 500:
            break
    transaction.commit()

class Command(BaseCommand):

    help = "Import an Anthropology Museum catalogue"

    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("need exactly one argument for db directory")

        dir, = args

        management.call_command('reset', 'cat', interactive=False)
        management.call_command('syncdb', interactive=False)

        import_csv(dir)

        

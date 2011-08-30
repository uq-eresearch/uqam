from django.core.management.base import BaseCommand, CommandError
from cat.models import MuseumObject,FunctionalCategory
from django.core import management

import csv
import sys
import os

ARTEFACT_CSV = 'Artefact.csv'

def prepare_stdout():
    unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbuffered

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
        fc, created = FunctionalCategory.objects.get_or_create(name=r['Functional_Category'])
        m.functional_category = fc
        m.description = r["Description"]
        m.comment = r["Comment"]
        m.country = r["Country_Name"]
        m.save()

        count += 1
        if count > 500:
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

        import_csv(dir)

        

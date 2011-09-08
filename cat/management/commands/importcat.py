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
ARTEFACT_MORE_CSV = 'ACCESS2_Artefact_More.csv'
DONOR_CSV = 'Donor.csv'

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
    print ("Importing People")

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
def process_csv(filename, row_handler):
    '''Read each line of a csv and process with the supplied function'''
    try:
        with open(filename) as f:
            data = csv.DictReader(f)
            count = 0
            print ('Importing from ', filename)
            for row in data:
                sys.stdout.write('.')
                row_handler(row)
                count+=1
                sys.stdout.write('%d\n' % count)
                if (count % 1000) == 0:
                    transaction.commit()
    except:
        print "Unexpected error: ", sys.exc_info()
    else:
        transaction.commit()

def process_artefactmore_record(r):
    '''Save details from an Artefact More.csv row into an Artefact Model'''
    m = MuseumObject.objects.get(pk=r['Artefact_Registration'])
    m.indigenous_name = r['Indigenous_Name']
    m.recorded_use = r['Recorded_Use']
    m.raw_material = r['Raw_Material']
    m.assoc_cultural_group = r['Assoc_Cultural_Group']
    m.maker_or_artist = r['Maker_Artist']

    def mapint(attr, fieldname):
        try:
            setattr(m, attr, int(r[fieldname]))
        except ValueError:
            pass

    mapint('width', 'Width(mm)')
    mapint('length', 'Length(mm)')
    mapint('height', 'Height(mm)')
    mapint('depth', 'Depth(mm)')
    mapint('circumference', 'Circumference(mm)')
    mapint('longitude', 'Longitude')
    mapint('latitude', 'Latitude')

    m.site_name_number = r['Site_Name_Nmbr']
    m.save()

def process_donorrecord(row):
    m = MuseumObject.objects.get(pk=row['Artefact_Registration'])
    p = Person.objects.get(pk=int(row["Person_idnbr"]))
    m.donor = p
    m.how_donor_obtained = row['How_obtained']
    m.when_donor_obtained = row['When_obtained']
    m.save()
    

def process_artefact_record(r):
    r = clean_row(r)

    m = MuseumObject()

    # Map simple fields
    m.registration_number = r["Reg_counter"]
    m.registration_number = r["Artefact_Registration"]
    m.old_registration_number = r["Old_Registration_nmbr"]
    m.other_number = r["Other_nmbr"]
    if r["Aquisition_Date"] != "":
        m.acquisition_date = r["Aquisition_Date"]
    m.acquisition_method = r["Aquisition_Method"]
    m.access_status = r["AccessStatus"]
    m.loan_status = r["Loan_Status"]
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

    try:
        p = Person.objects.get(pk=int(r["Collector_photographerID"]))
        m.collector = p
    except:
        print("Could not find collector: ", r["Collector_photographerID"])
        print(sys.exc_info())
#        import pdb
#        pdb.set_trace()

#    print (m.registration_number)
    m.save()

class Command(BaseCommand):

    help = "Import an Anthropology Museum catalogue"

    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("need exactly one argument for db directory")

        dir, = args

        management.call_command('reset', 'cat', interactive=False)
        management.call_command('reset', 'mediaman', interactive=False)
        management.call_command('syncdb', interactive=False)

        prepare_stdout()

        import_people(dir)
        process_csv(dir + ARTEFACT_CSV, process_artefact_record)
        process_csv(dir + ARTEFACT_MORE_CSV, process_artefactmore_record)
        process_csv(dir + DONOR_CSV, process_donorrecord)
        #import_artefact_more(dir)

        

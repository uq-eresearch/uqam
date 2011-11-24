from django.core.management.base import BaseCommand, CommandError
from cat.models import MuseumObject, FunctionalCategory, ArtefactType, CulturalBloc
from cat.models import Person, Place, Region, Category
from loans.models import LoanAgreement, LoanItem, Client
from condition.models import ConditionReport, ConservationAction, Deaccession, Conservator
from dataimport.models import ImportIssue
from django.core import management
from django.db import transaction
from django import db
from os.path import join
import re
import csv
import sys
import os
import string


def prepare_stdout():
    unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = unbuffered

def clean_row(row):
    row["Functional_Category"] = string.capwords(row["Functional_Category"])
    row["Loan_Status"] = string.capwords(row["Loan_Status"])
    return row

@transaction.commit_manually
def process_csv(filename, row_handler):
    '''Read each line of a csv and process with the supplied function'''
    db.reset_queries() # Don't leak memory by forever storing SQL queries
    try:
        with open(filename) as f:
            data = csv.DictReader(f)
            count = 0
            print 'Importing from ', filename
            for row in data:
                for key,value in row.items():
                    row[key] = value.strip()
                count+=1
                sys.stdout.write('\r{0}'.format(count))
                row_handler(row)
                if (count % 1000) == 0:
                    transaction.commit()
    except:
        print "\nUnexpected error: ", sys.exc_info()
    else:
        transaction.commit()
    print("")

def process_person_record(r):
    '''Read person records from a row of the csv and create DB records'''
    if r['Name'] == '':
        return
    p = Person()
    p.id = r["Person idnmbr"]
    p.name = r["Name"]
    p.comments = r["PersonComments"]
    p.save()

def process_artefactmore_record(r):
    '''Save details from an Artefact More.csv row into an Artefact Model'''
    m = MuseumObject.objects.get(registration_number=r['Artefact_Registration'])
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
    '''Update a museumobject record with details from a row of the donor csv'''
    m = MuseumObject.objects.get(registration_number=row['Artefact_Registration'])
    p = Person.objects.get(pk=int(row["Person_idnbr"]))
    m.donor_2 = p
    m.how_donor_obtained = row['How_obtained']
    m.when_donor_obtained = row['When_obtained']
    m.save()

def process_collectorphotographer_record(r):
    """
    Update a museumobject record with details from a row of the collectorphotog csv
    """
    m = MuseumObject.objects.get(registration_number=r['Artefact_Registration'])
    p = Person.objects.get(pk=int(r['Person_idnbr']))
    m.collector_2 = p
    m.how_collector_obtained = r['How_Obtained1']
    m.when_collector_obtained = r['When_Obtained1']
    m.save()

def process_artefacttype_record(r):
    a, created = ArtefactType.objects.get_or_create(name=r['Artefact_TypeName'])
    a.definition = r['Definition']
    a.see_also = r['SeeAlso']
    a.save()

def process_cultural_bloc_record(r):
    c,created = CulturalBloc.objects.get_or_create(name = r['CulturalBloc'])
    c.definition = r['Definition']
    c.save()

def process_functional_category_record(r):
    name = string.capwords(r['Functional_Category'])
    f,created = FunctionalCategory.objects.get_or_create(name=name)
    f.definition = r['Definition']
    f.save()

    

def process_artefact_record(r):
    r = clean_row(r)

    m = MuseumObject()

    # Map simple fields
    m.id = r["Artefact_Registration"]
    m.registration_number = r["Artefact_Registration"]
    m.old_registration_number = r["Old_Registration_nmbr"]
    m.reg_counter = r["Reg_counter"]
    m.other_number = r["Other_nmbr"]
    if r["Aquisition_Date"] != "":
        m.acquisition_date = r["Aquisition_Date"]
    m.acquisition_method = r["Aquisition_Method"]
    m.access_status = r["AccessStatus"]
    m.loan_status = r["Loan_Status"]
    m.description = r["Description"]
    m.comment = r["Comment"]
    m.storage_section = r['Storage_Section']
    m.storage_unit = r['Storage_Unit']
    m.storage_bay = r['Storage_Bay']
    m.storage_shelf_box_drawer = r['Shelf_Box_Drawer']

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
        print "\nCould not find collector: ", r["Collector_photographerID"]
#        print(sys.exc_info())
    try:
        p = Person.objects.get(pk=int(r["DonorID"]))
        m.donor = p
    except:
        print "\nCould not find donor: ", r["DonorID"]
#        print(sys.exc_info())

    m.save()

    # Set Category
    artefact_name = r['Artefact_TypeName']
    try:
        cat = Category.objects.get(name__iexact=artefact_name)
        m.category.add(cat)
        m.save()
    except Category.MultipleObjectsReturned:
        issue = ImportIssue(
                description="Multiple matching categories '%s'" % artefact_name,
                content_object=m)
        issue.save()
    except Category.DoesNotExist:
        issue = ImportIssue(
                description="Could not find category '%s'" % artefact_name,
                content_object=m)
        issue.save()

    m.save()


def process_loan_record(r):
    l = LoanAgreement()
    l.id = r['LoanId']
    l.date_borrowed = r['Borrowing_Date']
    l.return_date = r['Return_Date']
    l.approved_by, created = Person.objects.get_or_create(name=r['Approved by'])
    l.prepared_by, created = Person.objects.get_or_create(name=r['Prepared by'])
    l.clientNumber = r['ClientNumber']
    l.special_loan_conditions = r['Loan_Conditions']
    l.location = r['Location']
    l.loan_type = r['Loan Type']
    l.reason = r['Loan_Reason_type']
    l.returned = r['Returned']
    l.comments = r['Comments']
    l.client = Client.objects.get(id=r['ClientNumber'])
    l.save()

def process_client_record(r):
    c = Client()
    c.id = r['ClientNumber']
    c.name = string.join((r['Title'], r['FirstName(s)'], r['Surname']))
    c.organisation = r['Organisation']
    c.position = r['Position']
    c.address = string.join((r['AddressLine1'], r['AddressLine2'], r['AddressLine3']), "\n")
    c.town_suburb = r['Town/suburb']
    c.state = r['State']
    c.country = r['OverseasCountry']
    c.postcode = r['Postcode']
    c.phone1 = r['Phone1']
    c.phone2 = r['Phone2']
    c.save()
def process_loanitem_record(r):
    l = LoanItem()
    l.loan = LoanAgreement.objects.get(id=int(r['LoanId']))
    l.item = MuseumObject.objects.get(id=r['Artefact_Registration'])
    l.out_condition = r['ConditionCode']
    l.return_condition = r['Return_Condition']
    l.save()

def process_regioncombo(row):
    r, created = Region.objects.get_or_create(name=row['Region'])
    r.description = row['Definition']
    r.save()


def process_condition(r):
    c = ConditionReport()
    c.item = MuseumObject.objects.get(registration_number=r['Registration'])
    cond = r['ConditionCode']
    cond = re.sub(' ?- ?', ' - ', cond)
    c.condition = string.capwords(cond)
    if r['Condition_Date']:
        c.date = r['Condition_Date']
    c.details = r['Details']
    c.report_author,created = Person.objects.get_or_create(name=r['Report_Produced'])
    c.change_reason = r['Change_Reason']
    try:
        c.save()
    except:
        print("Error with condition report for item: %s" % c.item)
        print sys.exc_info()
        
def process_conservation(r):
    item = MuseumObject.objects.get(registration_number=r['Registration'])
    c, created = ConservationAction.objects.get_or_create(item=item, date=r['Action_Date'])
    c.action = r['Conservation_action']
    c.details = r['Action_Details']
    c.future_conservation = r['Future_Conservation']
    if r['Future_Conservation_Date']:
        c.future_conservation_date = r['Future_Conservation_Date']
    c.comments = r['Comments']
    c.material_used = r['Material_used']
    c.conservator = Conservator.objects.get(id=r['ConservatorId'])
    try:
        c.save()
    except:
        print("Error with conservation report for item: %s" % c.item)
        print sys.exc_info()
def process_deaccession(r):
    item = MuseumObject.objects.get(registration_number=r['Artefact_Registration'])
    person, created = Person.objects.get_or_create(name=r['Museum_StaffName'])

    d,created = Deaccession.objects.get_or_create(item=item,
                                                  person=person,
                                                  reason=r['Reason'])
    if r["Deaccession_Date"] != "":
        d.date = r['Deaccession_Date']
    d.save()

def process_museumstaff(r):
    p, created = Person.objects.get_or_create(name=r['Museum_StaffName'])
    if not created:
        p.comments = r['Details']
    else:
        p.comments = p.comments + '\n' + r['Details']

    p.save()

def process_conservator(r):
    c = Conservator()
    c.id = r['ConservatorId']
    c.title = r['Title']
    c.firstname = r['First_Name']
    c.surname = r['Surname']
    c.organisation = r['OrganisationName']
    c.email = r['Email']
    c.fax = r['Fax']
    c.phone = r['Phone1']
    c.save()

mappings = {
    'cat': (
        ('Region_combo.csv', process_regioncombo),
        ('Functional_Category.csv', process_functional_category_record),
        ('Artefact_type.csv', process_artefacttype_record),
        ('Cultural_Bloc_Combo.csv', process_cultural_bloc_record),
        ('Person.csv', process_person_record),
        ('Artefact.csv', process_artefact_record),
        ('ACCESS2_Artefact_More.csv', process_artefactmore_record),
        ('Donor.csv', process_donorrecord),
        ('Collector_Photographer.csv', process_collectorphotographer_record),
    ),
    'loans': (
        ('Client.csv', process_client_record),
        ('Loan.csv', process_loan_record),
        ('Artefacts_on_Loan.csv', process_loanitem_record),
    ),
    'condition': (
        ('Museum_Staff.csv', process_museumstaff),
        ('Conservator.csv', process_conservator),
        ('Conservation_Details.csv', process_conservation),
        ('Deaccession.csv', process_deaccession),
        ('Artefact_Condition.csv', process_condition)
    )
}

# Defined Dictionaries
# Access_Status_Combo, Aquisition_method_Combo, Artefact_type,
# Aust_State Combo, Condition_Combo, Conservation_action_Combo,
# Country_Combo (no definitions), Cultural_Bloc_Combo, Deacession_Reason_Combo,
# Functional_Category, Loan_Reason_Combo, Loan_Status_Combo, Obtained_Combo
# Photo_Type_Combo, Region_combo, 

def migrate_and_import(directory, appname, mapping):
#    management.call_command('reset', appname, interactive=False)
    management.call_command('migrate', appname, interactive=False)
    for filename, function in mapping[appname]:
        process_csv(join(directory, filename), function)

class Command(BaseCommand):

    help = "Import an Anthropology Museum catalogue"

    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError("Need at least two arguments. Import dir, and at least one app name")

        directory = args[0]
        prepare_stdout()

        for app_name in args[1:]:
            migrate_and_import(directory, app_name, mappings)

#        migrate_and_import(directory, 'cat', mappings)
#        migrate_and_import(directory, 'loans', loans)
#        migrate_and_import(directory, 'condition', condition)


